"""게이트 공통 계약 — 생성·피드백·재생성·재시도·승인 (KDEV-WORK-014 P3 / KDEV-SPEC-008·009).

스테이지마다 만드는 내용은 다르지만 **절차는 하나**다. 그래서 여기에 절차만 두고,
무엇을 만들지는 주입된 실행기(`StageRunner`) 가 안다. WORK-015 의 `source_note`·`concept`·`derived`
게이트가 이 파일을 그대로 재사용한다.

세 가지 상태를 섞지 않는 것이 이 모듈의 핵심 규율이다.

    gates.status           사람이 보는 단계 상태 (검토 대기 / 실패 / 승인…)
    gate_revisions.status  AI 제안 버전 상태 (drafting / reviewable / approved…)
    ai_tasks.status        실행 상태 (queued / running / succeeded / failed)

게이트가 `review_pending` 인데 실행은 `succeeded` 이고 버전은 `reviewable` 인 것이 정상이다.
하나로 합치면 *"AI 가 실패한 것"* 과 *"사람이 아직 안 본 것"* 이 구분되지 않는다.

**실행은 비동기다** (KDEV-WORK-016 / SPEC-009). 이 모듈의 함수들은 AI 를 기다리지 않는다.
`open_gate`·`regenerate`·`retry` 는 **제출까지만** 하고 즉시 돌아오며, 결과는 나중에
`harvest()` 가 채운다. 사람의 조작(피드백·승인)만 동기다 — 이미 만들어진 것을 저장하는
일이라 즉시 끝난다.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Protocol

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import AITask, Gate, GateFeedback, GateRevision, ItemPreparation, QueueItem

from .definitions import pipeline_for
from .executor import Execution

logger = logging.getLogger("kknaks-back.pipeline.gates")

#: 한 단어 피드백으로는 방향이 전달되지 않는다 (SPEC-009 Validation).
MIN_FEEDBACK_LENGTH = 4

#: 재생성을 받을 수 있는 게이트 상태.
REGENERATABLE = ("review_pending", "feedback_pending")

#: 실행을 제출해 놓고 결과를 기다리는 게이트 상태 — 수확 대상이다.
IN_FLIGHT = ("generating", "regenerating")


class GateError(RuntimeError):
    """사용자에게 코드로 알려야 하는 게이트 조작 오류."""

    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code
        self.message = message or code


@dataclass(frozen=True)
class GenerationInput:
    """실행기가 제안을 만들 때 받는 것 전부. 제출과 수확 양쪽에서 같은 것을 받는다."""

    item: QueueItem
    gate: Gate
    preparation: ItemPreparation | None
    previous_payload: dict[str, Any] | None
    feedback: str | None
    #: 이어받을 세션. 없으면 실행기가 stateless 로 만들어야 한다(SPEC-009 S-5).
    #: **앞 스테이지의 것일 수 있다** — 체인 하나가 한 대화다(KDEV-DEC-024 D1).
    session_ref: str | None
    #: 승인된 route 결과. 뒤 스테이지는 목적지·group 을 여기서 읽는다.
    #: 실행기에 DB 를 넘기지 않기 위해 조립 시점에 채워 준다.
    route: dict[str, Any] | None = None
    #: 앞 스테이지가 이미 승인받은 산출물 — concept 가 reference stem 을 `up:` 으로
    #: 걸려면 이게 필요하다. 계보는 같은 발행 묶음 안에서 만들어진다.
    upstream: dict[str, Any] | None = None
    #: 직전 실패 사유. **재시도에서만** 채워진다 (KDEV-DEC-024 D3).
    #: 사람 피드백(`feedback`)과 섞지 않는다 — 출처가 다르고, 섞으면 사람이 하지 않은
    #: 말이 「사용자 지적」으로 화면에 남는다.
    retry_error: str | None = None


class StageRunner(Protocol):
    """스테이지 실행기 — **제출과 수확이 나뉘어 있다** (SPEC-009 「실행은 비동기다」).

    `submit` 은 큐에 넣고 `task_id` 만 돌려준다. `poll` 은 기다리지 않고 지금 상태만
    본다. `parse` 는 완료된 원문을 payload 로 바꾸며, 어긋나면 `GateError` 를 던진다.
    """

    async def submit(self, request: GenerationInput) -> str: ...

    async def poll(self, task_id: str) -> Execution: ...

    def parse(self, raw: str, request: GenerationInput) -> dict[str, Any]: ...


def _now() -> datetime:
    return datetime.now(timezone.utc)


async def latest_preparation(db: AsyncSession, item_id: int) -> ItemPreparation | None:
    return await db.scalar(
        select(ItemPreparation)
        .where(ItemPreparation.item_id == item_id, ItemPreparation.status == "succeeded")
        .order_by(ItemPreparation.version.desc())
        .limit(1)
    )


async def approved_route_payload(db: AsyncSession, item_id: int) -> dict[str, Any] | None:
    """승인된 route 결과. 없으면 `None` — 아직 목적지가 안 정해진 항목이다."""
    gate = await db.scalar(
        select(Gate)
        .where(Gate.item_id == item_id, Gate.stage_name == "route", Gate.status == "approved")
        .limit(1)
    )
    if gate is None or gate.approved_revision_id is None:
        return None
    revision = await db.get(GateRevision, gate.approved_revision_id)
    return revision.payload if revision else None


async def upstream_context(db: AsyncSession, item_id: int) -> dict[str, Any]:
    """이 항목에서 **이미 승인된** 앞 스테이지 산출물의 요약.

    아직 승인 전인 것은 넣지 않는다 — 바뀔 수 있는 값을 상류로 걸면 계보가 거짓이 된다.
    """
    rows = (
        await db.execute(
            select(Gate.stage_name, GateRevision.payload)
            .join(GateRevision, GateRevision.id == Gate.approved_revision_id)
            .where(Gate.item_id == item_id, Gate.status == "approved")
        )
    ).all()
    context: dict[str, Any] = {}
    for stage_name, payload in rows:
        if stage_name == "source_note" and isinstance(payload, dict):
            context["source_note_stem"] = payload.get("filename_stem")
    return context


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


async def _gate_session(db: AsyncSession, gate_id: int) -> str | None:
    """게이트 하나가 남긴 최신 세션 — 버전에 없으면 그 게이트의 실행 기록까지.

    **실행 기록을 게이트로 좁혀 찾는다.** 종전에는 `AITask.kind == stage_name` 으로
    찾았는데 그 축은 **게이트가 살아 있는지를 모른다** — route 재오픈으로 취소된
    옛 게이트의 세션이 그대로 걸렸다(KDEV-DEC-024 D2).

    실패한 실행의 세션도 여기서 걸린다. 그게 의도다 — 형식이 틀려 죽은 실행은 세션이
    남아 있고, 재시도가 물고 싶은 것이 정확히 그것이다(D3).
    """
    from_revision = await db.scalar(
        select(GateRevision.session_ref)
        .where(GateRevision.gate_id == gate_id, GateRevision.session_ref.is_not(None))
        .order_by(GateRevision.version.desc())
        .limit(1)
    )
    if from_revision:
        return from_revision
    return await db.scalar(
        select(AITask.session_ref)
        .join(GateRevision, GateRevision.ai_task_id == AITask.id)
        .where(GateRevision.gate_id == gate_id, AITask.session_ref.is_not(None))
        .order_by(AITask.id.desc())
        .limit(1)
    )


async def _resume_session(db: AsyncSession, gate: Gate, *, source_kind: str) -> str | None:
    """이어받을 세션을 찾는다 (SPEC-009 S-5·S-6 / KDEV-DEC-024 D1).

        ① 이 게이트의 최신 버전 세션        재생성
        ② 이 게이트의 최신 실행 세션        재시도 — 형식 실패의 세션이 여기 있다
        ③ **앞 게이트의 세션**              정의 역순, 가장 가까운 것부터
        ④ 없으면 None                       호출자가 stateless 로 만든다

    ③이 이 함수의 새 몫이다. 그전까지는 스테이지가 넘어가면 무조건 새 세션이라
    매 스테이지가 규칙·양식을 다시 읽고 원문을 다시 받았다 — 13분의 상당 부분이
    거기였다. 이제 `concept` 는 「방금 내가 쓴 자료 노트」를 딛는다.

    **`cancelled` 게이트는 건너뛴다.** 재오픈으로 무효화된 대화는 틀린 목적지 위에서
    쓴 것이고, 그것을 물면 재오픈이 한 일이 반쯤 취소된다(D2).

    끝내 없으면 `None`. **실패시키지 않는다** — 웜을 전제로만 도는 경로를 만들지
    않는다(D4).
    """
    own = await _gate_session(db, gate.id)
    if own:
        return own

    pipeline = pipeline_for(source_kind)
    if pipeline is None:
        return None
    order = [stage.name for stage in pipeline.gate_stages()]
    if gate.stage_name not in order:
        return None

    for name in reversed(order[: order.index(gate.stage_name)]):
        earlier = await live_gate(db, gate.item_id, name)
        if earlier is None:
            continue
        session = await _gate_session(db, earlier.id)
        if session:
            return session
    return None


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
    runner: StageRunner,
) -> Gate | None:
    """스테이지 게이트를 열고 첫 제안을 **제출한다.**

    돌아올 때 게이트는 `generating` 이다. 내용은 아직 없다 — 수확이 채운다.
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
    await _submit(db, gate, item=item, runner=runner)
    return gate


async def open_first_gate(
    db: AsyncSession, item: QueueItem, *, runner: StageRunner
) -> Gate | None:
    pipeline = pipeline_for(item.source_kind)
    stage = pipeline.first_gate() if pipeline else None
    if stage is None:
        return None
    return await open_gate(db, item, stage.name, runner=runner)


async def _generation_input(
    db: AsyncSession,
    gate: Gate,
    *,
    item: QueueItem,
    feedback: GateFeedback | None,
    parent: GateRevision | None,
    retry_error: str | None = None,
) -> GenerationInput:
    """스테이지가 받는 입력을 **DB 에서 조립한다.**

    제출 시점과 수확 시점 양쪽에서 만든다. 제출 때 만든 것을 메모리에 붙잡아 두면
    back 재시작 뒤에는 수확할 재료가 사라진다 — 실행기 큐에 작업이 남아 있어도
    결과를 해석하지 못하게 된다.

    `retry_error` 만 예외적으로 **제출 쪽에서만** 온다. 수확이 쓰는 것은 `parse` 뿐이고
    그쪽은 이 값을 보지 않는다 — 재조립 대상이 아니다.
    """
    return GenerationInput(
        item=item,
        gate=gate,
        preparation=await latest_preparation(db, gate.item_id),
        previous_payload=parent.payload if parent else None,
        feedback=feedback.body if feedback else None,
        session_ref=await _resume_session(db, gate, source_kind=item.source_kind),
        route=await approved_route_payload(db, gate.item_id),
        upstream=await upstream_context(db, gate.item_id),
        retry_error=retry_error,
    )


async def _fail(
    db: AsyncSession,
    gate: Gate,
    task: AITask,
    revision: GateRevision,
    *,
    error_code: str,
    error_message: str,
    session_ref: str | None = None,
) -> GateRevision:
    """실패해도 **행을 남긴다** — 왜 막혔는지가 재시도 판단의 근거다.

    **세션도 남긴다** (KDEV-DEC-024 D3). 파싱·검증 실패는 실행이 성공한 **뒤에** 나는
    것이라 세션이 손에 있고, 재시도가 물고 싶은 것이 정확히 그것이다 — 자료를 처음부터
    다시 읽는 대신 방금 낸 출력을 고치게 된다.

    실행 자체가 실패한 경우(timeout·작업 소실)에는 값이 안 들어와 자연히 새 세션이
    된다. **사유 목록으로 분기하지 않는다** — 「세션이 저장돼 있는가」가 곧 그 판정이다.
    """
    task.status = "failed"
    task.error_code = error_code
    task.error_message = error_message[:1000]
    task.session_ref = session_ref
    task.finished_at = _now()
    revision.status = "failed"
    gate.status = "failed"
    await db.flush()
    return revision


async def _submit(
    db: AsyncSession,
    gate: Gate,
    *,
    item: QueueItem,
    runner: StageRunner,
    feedback: GateFeedback | None = None,
    parent: GateRevision | None = None,
    retry_of: AITask | None = None,
    retry_error: str | None = None,
) -> GateRevision:
    """제안 하나를 **제출만** 한다 (SPEC-009 「실행은 비동기다」).

    나가는 것은 `task_id` 뿐이고, 그 자리에서 커밋할 수 있는 상태로 돌아온다.
    AI 를 여기서 기다리면 앞단 프록시가 끊고 트랜잭션이 통째로 롤백된다.
    """
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

    try:
        request = await _generation_input(
            db, gate, item=item, feedback=feedback, parent=parent, retry_error=retry_error
        )
        task_id = await runner.submit(request)
    except Exception as exc:  # noqa: BLE001 — 실패는 상태이지 예외 전파가 아니다
        return await _fail(
            db,
            gate,
            task,
            revision,
            error_code=type(exc).__name__,
            error_message=str(exc),
        )

    # 이 한 줄이 재시작 내성의 전부다 — 작업은 실행기 큐에 있고, 여기 참조가 남는다.
    task.external_task_ref = str(task_id)
    await db.flush()
    return revision


async def harvest(
    db: AsyncSession, gate: Gate, *, item: QueueItem, runner: StageRunner
) -> bool:
    """제출해 둔 실행을 확인해 끝났으면 결과를 채운다. 바뀌었으면 `True`.

    **멱등이어야 한다.** 화면 폴링이 겹쳐 두 요청이 동시에 들어와도 revision 이 두 번
    채워지면 안 된다. 그래서 `drafting` 행을 `FOR UPDATE` 로 잡는다 — 두 번째 요청은
    첫 번째가 끝날 때까지 기다렸다가, 조건이 더는 맞지 않으므로 그냥 돌아간다.

    아직 실행 중이면 아무것도 바꾸지 않고 `False`.
    """
    if gate.status not in IN_FLIGHT:
        return False

    revision = await db.scalar(
        select(GateRevision)
        .where(GateRevision.gate_id == gate.id, GateRevision.status == "drafting")
        .order_by(GateRevision.version.desc())
        .limit(1)
        .with_for_update()
    )
    if revision is None:
        # **먼저 온 수확이 이미 끝냈을 수 있다.** 화면 폴링과 드라이버가 같은 게이트를
        # 함께 민다 — 앞선 쪽이 `drafting` 을 `reviewable` 로 바꾸고 나면 늦은 쪽에는
        # 초안이 안 보인다. 그걸 실패로 읽으면 **성공한 게이트가 failed 로 뒤집힌다.**
        #
        # 운영에서 그랬다. 개념 게이트가 `failed` 인데 그 버전은 `reviewable` 이고
        # AI 작업도 `succeeded` 라, 화면은 「검토 대기」로 그리면서 승인은
        # 「상태가 failed 라 승인할 수 없다」로 막혔다.
        done = await db.scalar(
            select(GateRevision)
            .where(GateRevision.gate_id == gate.id, GateRevision.status == "reviewable")
            .order_by(GateRevision.version.desc())
            .limit(1)
        )
        if done is not None:
            gate.status = "review_pending"
            gate.active_revision_id = done.id
            await db.flush()
            return True

        # 정말로 없다 — 제출이 커밋 전에 끊긴 흔적이므로 사람이 재시도할 수 있게 닫는다.
        logger.warning("게이트 %s 가 %s 인데 drafting 버전이 없다", gate.id, gate.status)
        gate.status = "failed"
        await db.flush()
        return True

    task = await db.get(AITask, revision.ai_task_id) if revision.ai_task_id else None
    if task is None:
        gate.status = "failed"
        revision.status = "failed"
        await db.flush()
        return True
    if not task.external_task_ref:
        await _fail(
            db,
            gate,
            task,
            revision,
            error_code="TASK_REF_MISSING",
            error_message="제출 기록에 실행기 작업 참조가 없다",
        )
        return True

    execution = await runner.poll(task.external_task_ref)
    if execution.running:
        return False
    if execution.status == "failed":
        await _fail(
            db,
            gate,
            task,
            revision,
            error_code=execution.error_code or "EXECUTION_FAILED",
            error_message=execution.error_message or "실행이 실패했다",
        )
        return True

    feedback = (
        await db.get(GateFeedback, revision.feedback_id) if revision.feedback_id else None
    )
    parent = (
        await db.get(GateRevision, revision.parent_revision_id)
        if revision.parent_revision_id
        else None
    )
    try:
        request = await _generation_input(
            db, gate, item=item, feedback=feedback, parent=parent
        )
        payload = runner.parse(execution.result or "", request)
    except Exception as exc:  # noqa: BLE001 — 파싱·검증 실패도 실행 실패와 같이 다룬다
        code = exc.code if isinstance(exc, GateError) else type(exc).__name__
        # 실행은 끝났으므로 세션이 있다. 재시도가 그것을 물고 사유를 받는다(DEC-024 D3).
        await _fail(
            db,
            gate,
            task,
            revision,
            error_code=code,
            error_message=str(exc),
            session_ref=execution.session_ref,
        )
        return True

    task.status = "succeeded"
    task.session_ref = execution.session_ref
    task.finished_at = _now()

    revision.payload = payload
    revision.session_ref = execution.session_ref
    # 검토 가능이 되기 **직전** 형제를 밀어낸다 — 순서가 반대면 잠시 0개가 된다.
    await _sweep_reviewable(db, gate.id, keep_revision_id=revision.id)
    revision.status = "reviewable"

    gate.status = "review_pending"
    gate.active_revision_id = revision.id
    if feedback is not None:
        feedback.status = "consumed"
    await db.flush()
    return True


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
    db: AsyncSession, gate: Gate, *, item: QueueItem, runner: StageRunner
) -> GateRevision:
    """피드백을 반영한 새 버전을 **제출한다.** 이전 버전은 고치지 않고 read-only 로 남는다."""
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
    return await _submit(
        db, gate, item=item, runner=runner, feedback=feedback, parent=parent
    )


async def retry(db: AsyncSession, gate: Gate, *, item: QueueItem, runner: StageRunner):
    """실패한 생성을 다시 **제출한다.** 기존 실패 기록은 수정하지 않는다 (SPEC-009 S-4)."""
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
    return await _submit(
        db,
        gate,
        item=item,
        runner=runner,
        feedback=feedback,
        parent=last_revision,
        retry_of=last_failed,
        # **직전 실패 사유를 들려 보낸다** (KDEV-DEC-024 D3). 형식이 틀렸다면 그 세션을
        # 물고 시작하므로, 자료를 다시 읽는 대신 방금 낸 출력을 고치는 일이 된다.
        retry_error=(last_failed.error_message if last_failed else None),
    )


#: 스테이지별로 **승인이 지워서는 안 되는** 최상위 키.
#:
#: `payload_override` 는 통째 교체다. 화면이 키를 빠뜨리면 그 산출물이 조용히
#: 사라지고, 사람은 「승인됨」을 본 채로 발행에서야 `EMPTY_PLAN` 을 만난다.
#: 실제로 잔디 게이트가 그렇게 당했다 — 화면의 concept 판정이 잔디 payload 를
#: 삼켜 `{concepts}` 만 보냈고 `daily`·`career` 가 버려졌다(결함 ⑧).
#:
#: **route 는 넣지 않는다.** `validate_route_result` 가 비어 있는 `rationale` 을
#: 정당하게 떨어뜨리므로 여기 걸면 멀쩡한 승인이 막힌다.
REQUIRED_PAYLOAD_KEYS: dict[str, tuple[str, ...]] = {"daily": ("daily",)}


def _check_override_keeps_outputs(
    gate: Gate, revision: GateRevision, override: dict[str, Any]
) -> None:
    """사람이 고친 payload 가 산출물을 통째로 지우지 않았는지.

    값이 바뀌는 것은 편집이고 정상이다. **키가 사라지는 것은 편집이 아니다.**
    """
    required = REQUIRED_PAYLOAD_KEYS.get(gate.stage_name)
    if not required or not isinstance(revision.payload, dict):
        return
    missing = [
        key for key in required if key in revision.payload and key not in override
    ]
    if missing:
        raise GateError(
            "PAYLOAD_KEYS_DROPPED",
            f"승인 payload 에서 산출물이 빠졌다 — {', '.join(missing)}. "
            "편집은 값을 바꾸는 것이지 산출물을 지우는 것이 아니다",
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
        _check_override_keeps_outputs(gate, revision, payload_override)
        revision.payload = payload_override
    revision.status = "approved"
    gate.status = "approved"
    gate.approved_revision_id = revision.id
    await db.flush()
    return revision
