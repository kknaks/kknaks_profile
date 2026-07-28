"""게이트 공통 계약 — 생성·피드백·재생성·재시도·승인 (KDEV-WORK-014 P3 / KDEV-SPEC-008·009).

스테이지마다 만드는 내용은 다르지만 **절차는 하나**다. 그래서 여기에 절차만 두고,
무엇을 만들지는 주입된 `generator` 가 안다. WORK-015 의 `source_note`·`concept`·`derived`
게이트가 이 파일을 그대로 재사용한다.

세 가지 상태를 섞지 않는 것이 이 모듈의 핵심 규율이다.

    gates.status           사람이 보는 단계 상태 (검토 대기 / 실패 / 승인…)
    gate_revisions.status  AI 제안 버전 상태 (drafting / reviewable / approved…)
    ai_tasks.status        실행 상태 (queued / running / succeeded / failed)

게이트가 `review_pending` 인데 실행은 `succeeded` 이고 버전은 `reviewable` 인 것이 정상이다.
하나로 합치면 *"AI 가 실패한 것"* 과 *"사람이 아직 안 본 것"* 이 구분되지 않는다.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import AITask, Gate, GateFeedback, GateRevision, ItemPreparation, QueueItem

from .definitions import pipeline_for

#: 한 단어 피드백으로는 방향이 전달되지 않는다 (SPEC-009 Validation).
MIN_FEEDBACK_LENGTH = 4

#: 재생성을 받을 수 있는 게이트 상태.
REGENERATABLE = ("review_pending", "feedback_pending")


class GateError(RuntimeError):
    """사용자에게 코드로 알려야 하는 게이트 조작 오류."""

    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code
        self.message = message or code


@dataclass(frozen=True)
class GenerationInput:
    """generator 가 제안을 만들 때 받는 것 전부."""

    item: QueueItem
    gate: Gate
    preparation: ItemPreparation | None
    previous_payload: dict[str, Any] | None
    feedback: str | None
    #: 이어받을 세션. 없으면 generator 가 stateless 로 만들어야 한다(SPEC-009 S-5).
    session_ref: str | None


@dataclass(frozen=True)
class GenerationResult:
    payload: dict[str, Any]
    session_ref: str | None = None
    external_task_ref: str | None = None


Generator = Callable[[GenerationInput], Awaitable[GenerationResult]]


def _now() -> datetime:
    return datetime.now(timezone.utc)


async def latest_preparation(db: AsyncSession, item_id: int) -> ItemPreparation | None:
    return await db.scalar(
        select(ItemPreparation)
        .where(ItemPreparation.item_id == item_id, ItemPreparation.status == "succeeded")
        .order_by(ItemPreparation.version.desc())
        .limit(1)
    )


async def live_gate(db: AsyncSession, item_id: int, stage_name: str) -> Gate | None:
    return await db.scalar(
        select(Gate)
        .where(Gate.item_id == item_id, Gate.stage_name == stage_name, Gate.status != "cancelled")
        .limit(1)
    )


async def _next_version(db: AsyncSession, gate_id: int) -> int:
    current = await db.scalar(
        select(func.max(GateRevision.version)).where(GateRevision.gate_id == gate_id)
    )
    return (current or 0) + 1


async def _resume_session(db: AsyncSession, gate: Gate) -> str | None:
    """이어받을 세션을 찾는다 — 버전에 없으면 실행 기록까지 뒤진다 (SPEC-009 S-5 2단계).

    끝내 없으면 `None`. 호출자는 실패시키지 않고 stateless 로 만든다.
    """
    from_revision = await db.scalar(
        select(GateRevision.session_ref)
        .where(GateRevision.gate_id == gate.id, GateRevision.session_ref.is_not(None))
        .order_by(GateRevision.version.desc())
        .limit(1)
    )
    if from_revision:
        return from_revision
    return await db.scalar(
        select(AITask.session_ref)
        .where(
            AITask.item_id == gate.item_id,
            AITask.kind == gate.stage_name,
            AITask.session_ref.is_not(None),
        )
        .order_by(AITask.id.desc())
        .limit(1)
    )


async def _sweep_reviewable(db: AsyncSession, gate_id: int, keep_revision_id: int) -> int:
    """같은 게이트의 다른 **검토 가능** 버전을 밀어낸다 (SPEC-009 S-3).

    게이트당 검토 대상은 항상 하나여야 한다. 이걸 DB 제약이 아니라 앱이 하는 이유는
    전이 순간에 잠깐 둘이 공존하기 때문이다 — 제약으로 걸면 정상 흐름이 막힌다.

    **`drafting`(생성 중) 은 건드리지 않는다.** 아직 검토 대상이 아니고, 밀어내면
    지금 돌고 있는 재생성이 완료 시점에 이미 죽어 있게 된다.
    """
    result = await db.execute(
        update(GateRevision)
        .where(
            GateRevision.gate_id == gate_id,
            GateRevision.id != keep_revision_id,
            GateRevision.status == "reviewable",
        )
        .values(status="superseded")
    )
    return result.rowcount or 0


async def open_gate(
    db: AsyncSession,
    item: QueueItem,
    stage_name: str,
    *,
    generator: Generator,
) -> Gate | None:
    """스테이지 게이트를 열고 첫 제안을 만든다.

    파이프라인 정의가 없는 입력 종류면 `None` — 게이트 없이 큐에 남는다.
    """
    pipeline = pipeline_for(item.source_kind)
    if pipeline is None:
        return None

    existing = await live_gate(db, item.id, stage_name)
    if existing is not None:
        return existing

    gate = Gate(
        item_id=item.id,
        stage_name=stage_name,
        stage_no=pipeline.stage_no(stage_name),
        status="generating",
    )
    db.add(gate)
    await db.flush()
    await _generate(db, gate, item=item, generator=generator)
    return gate


async def open_first_gate(
    db: AsyncSession, item: QueueItem, *, generator: Generator
) -> Gate | None:
    pipeline = pipeline_for(item.source_kind)
    stage = pipeline.first_gate() if pipeline else None
    if stage is None:
        return None
    return await open_gate(db, item, stage.name, generator=generator)


async def _generate(
    db: AsyncSession,
    gate: Gate,
    *,
    item: QueueItem,
    generator: Generator,
    feedback: GateFeedback | None = None,
    parent: GateRevision | None = None,
    retry_of: AITask | None = None,
) -> GateRevision:
    """제안 하나를 만든다. 실패해도 **행을 남긴다** — 왜 막혔는지가 재시도 판단의 근거다."""
    version = await _next_version(db, gate.id)
    task = AITask(
        item_id=gate.item_id,
        kind=gate.stage_name,
        status="running",
        retry_of_task_id=retry_of.id if retry_of else None,
    )
    db.add(task)
    await db.flush()

    revision = GateRevision(
        gate_id=gate.id,
        version=version,
        status="drafting",
        parent_revision_id=parent.id if parent else None,
        feedback_id=feedback.id if feedback else None,
        ai_task_id=task.id,
    )
    db.add(revision)
    await db.flush()

    preparation = await latest_preparation(db, gate.item_id)
    try:
        result = await generator(
            GenerationInput(
                item=item,
                gate=gate,
                preparation=preparation,
                previous_payload=parent.payload if parent else None,
                feedback=feedback.body if feedback else None,
                session_ref=await _resume_session(db, gate),
            )
        )
    except Exception as exc:  # noqa: BLE001 — 실패는 상태이지 예외 전파가 아니다
        task.status = "failed"
        task.error_code = type(exc).__name__
        task.error_message = str(exc)[:1000]
        task.finished_at = _now()
        revision.status = "failed"
        gate.status = "failed"
        await db.flush()
        return revision

    task.status = "succeeded"
    task.session_ref = result.session_ref
    task.external_task_ref = result.external_task_ref
    task.finished_at = _now()

    revision.payload = result.payload
    revision.session_ref = result.session_ref
    # 검토 가능이 되기 **직전** 형제를 밀어낸다 — 순서가 반대면 잠시 0개가 된다.
    await _sweep_reviewable(db, gate.id, keep_revision_id=revision.id)
    revision.status = "reviewable"

    gate.status = "review_pending"
    gate.active_revision_id = revision.id
    if feedback is not None:
        feedback.status = "consumed"
    await db.flush()
    return revision


async def submit_feedback(db: AsyncSession, gate: Gate, body: str) -> GateFeedback:
    if gate.status == "approved":
        raise GateError("GATE_ALREADY_APPROVED", "승인된 단계는 변경할 수 없다")
    if len((body or "").strip()) < MIN_FEEDBACK_LENGTH:
        raise GateError("FEEDBACK_TOO_SHORT", "수정 방향을 조금 더 구체적으로 적어야 한다")

    feedback = GateFeedback(
        gate_id=gate.id,
        target_revision_id=gate.active_revision_id,
        body=body.strip(),
        status="submitted",
    )
    db.add(feedback)
    gate.status = "feedback_pending"
    await db.flush()
    return feedback


async def regenerate(
    db: AsyncSession, gate: Gate, *, item: QueueItem, generator: Generator
) -> GateRevision:
    """피드백을 반영한 새 버전. 이전 버전은 고치지 않고 read-only 로 남는다."""
    if gate.status == "approved":
        raise GateError("GATE_ALREADY_APPROVED", "승인된 단계는 변경할 수 없다")
    if gate.status not in REGENERATABLE:
        raise GateError("RETRY_NOT_ALLOWED", f"상태가 {gate.status} 라 재생성할 수 없다")

    feedback = await db.scalar(
        select(GateFeedback)
        .where(GateFeedback.gate_id == gate.id, GateFeedback.status == "submitted")
        .order_by(GateFeedback.id.desc())
        .limit(1)
    )
    parent = (
        await db.get(GateRevision, gate.active_revision_id) if gate.active_revision_id else None
    )
    gate.status = "regenerating"
    await db.flush()
    return await _generate(
        db, gate, item=item, generator=generator, feedback=feedback, parent=parent
    )


async def retry(db: AsyncSession, gate: Gate, *, item: QueueItem, generator: Generator):
    """실패한 생성을 다시 돌린다. 기존 실패 기록은 수정하지 않는다 (SPEC-009 S-4)."""
    if gate.status != "failed":
        raise GateError("RETRY_NOT_ALLOWED", f"상태가 {gate.status} 라 재시도할 수 없다")

    last_failed = await db.scalar(
        select(AITask)
        .where(
            AITask.item_id == gate.item_id,
            AITask.kind == gate.stage_name,
            AITask.status == "failed",
        )
        .order_by(AITask.id.desc())
        .limit(1)
    )
    last_revision = await db.scalar(
        select(GateRevision)
        .where(GateRevision.gate_id == gate.id, GateRevision.status != "failed")
        .order_by(GateRevision.version.desc())
        .limit(1)
    )
    feedback = await db.scalar(
        select(GateFeedback)
        .where(GateFeedback.gate_id == gate.id, GateFeedback.status == "submitted")
        .order_by(GateFeedback.id.desc())
        .limit(1)
    )
    gate.status = "generating"
    await db.flush()
    return await _generate(
        db,
        gate,
        item=item,
        generator=generator,
        feedback=feedback,
        parent=last_revision,
        retry_of=last_failed,
    )


async def approve(
    db: AsyncSession,
    gate: Gate,
    *,
    payload_override: dict[str, Any] | None = None,
    expected_revision_id: int | None = None,
) -> GateRevision:
    """검토 중인 버전을 승인한다.

    `payload_override` 는 화면에서 토글을 바꾼 경우다 — AI 제안을 그대로 받는 것이
    아니라 **사람이 고친 결과가 승인 대상**이다. 그래서 승인된 버전에 반영해 둔다.

    `expected_revision_id` 는 낙관적 잠금이다. 다른 탭에서 재생성이 돌아 버전이 바뀌었는데
    옛 화면의 승인 버튼이 먹으면, 사람이 **보지 않은 내용을 승인**하게 된다.
    """
    if gate.status == "approved":
        raise GateError("GATE_ALREADY_APPROVED", "이미 승인된 단계다")
    if gate.status not in ("review_pending", "feedback_pending"):
        raise GateError("RETRY_NOT_ALLOWED", f"상태가 {gate.status} 라 승인할 수 없다")

    revision = (
        await db.get(GateRevision, gate.active_revision_id) if gate.active_revision_id else None
    )
    if revision is None or revision.status != "reviewable":
        raise GateError("STALE_REVISION", "검토 대상 버전이 없다")
    if expected_revision_id is not None and expected_revision_id != revision.id:
        raise GateError("STALE_REVISION", "화면이 보고 있는 버전이 최신이 아니다")

    if payload_override is not None:
        revision.payload = payload_override
    revision.status = "approved"
    gate.status = "approved"
    gate.approved_revision_id = revision.id
    await db.flush()
    return revision
