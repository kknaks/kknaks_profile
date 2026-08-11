"""Apply Executor — 승인된 것을 실제로 발행한다 (KDEV-WORK-015 P4 / KDEV-SPEC-010).

여기가 **처음으로 레포에 파일이 생기는 지점**이다. 그 앞까지는 전부 DB 안이었다.

순서가 중요하다.

    계획 조립 → 검증(파일 5종 + 그래프 L1~L6) → 쓰기 → 커밋 → push
                └ 하나라도 걸리면 파일을 쓰기 전에 전체 거부

검증을 쓰기 뒤로 미루면 "일부는 썼는데 거부" 상태가 생긴다. 그 상태를 되돌리는 것보다
안 만드는 편이 낫다.
"""

from __future__ import annotations

import logging
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ApplyPlan, ApplyResult, Gate, GateRevision, QueueItem

from .git import PublishOutcome, head_ref, publish_atomic, rollback
from .graph_check import check_graph
from .plan import FileAction, Violation, build_actions, validate_plan

logger = logging.getLogger("kknaks-back.apply.executor")


@dataclass(frozen=True)
class ApplyOutcome:
    status: str  # succeeded · rejected · failed
    result_id: int | None = None
    commit_ref: str | None = None
    violations: list[dict[str, str]] | None = None
    error_code: str | None = None
    error_message: str | None = None

    @property
    def ok(self) -> bool:
        return self.status == "succeeded"


async def approved_payloads(db: AsyncSession, item_id: int) -> dict[str, dict[str, Any]]:
    """승인된 게이트의 산출물만 모은다 — `cancelled` 는 제외된다."""
    rows = (
        await db.execute(
            select(Gate.stage_name, GateRevision.payload)
            .join(GateRevision, GateRevision.id == Gate.approved_revision_id)
            .where(
                Gate.item_id == item_id,
                Gate.status == "approved",
            )
        )
    ).all()
    return {stage: payload for stage, payload in rows if isinstance(payload, dict)}


def _write_all(repo_root: Path, actions: list[FileAction]) -> None:
    """계획을 작업트리에 쓴다. 원자적 교체로 반쯤 쓰인 파일을 남기지 않는다."""
    for action in actions:
        target = repo_root / action.path
        if action.action == "remove":
            # **없어도 정상이다.** 공부 노트는 접수 때 이미 입구에서 지워졌고, 여기서
            # 하는 일은 그 삭제를 커밋에 싣는 것뿐이다(`git add --` 가 삭제를 stage 한다).
            target.unlink(missing_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        handle, temp = tempfile.mkstemp(dir=str(target.parent), suffix=".tmp")
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as fh:
                fh.write(action.content)
            os.replace(temp, target)
        except BaseException:
            Path(temp).unlink(missing_ok=True)
            raise


def commit_message(item: QueueItem, actions: list[FileAction]) -> str:
    """발행 커밋 메시지 (DEC-012 OQ-1 해소).

    한 줄에 **무엇이 몇 장 나갔는지**가 보여야 `git log` 만으로 추적된다.
    본문에 항목 번호와 원문 URL 을 남겨 큐 기록과 이어 붙인다.
    """
    kinds: dict[str, int] = {}
    for action in actions:
        if action.action == "remove":
            # 회수는 **나간 장수가 아니다.** 제목의 숫자는 "무엇이 몇 장 나갔나" 이고,
            # 지워진 입구 원본이 거기 섞이면 그 숫자가 거짓말을 한다. 본문 줄에는 남는다.
            continue
        kinds[action.note_type or "unknown"] = kinds.get(action.note_type or "unknown", 0) + 1
    summary = " ".join(f"{k}:{v}" for k, v in sorted(kinds.items()))
    title = f"knowledge: publish item #{item.id} ({summary})"
    lines = [title, "", *(f"- {a.action} {a.path}" for a in actions)]
    if item.source_url:
        lines += ["", f"source: {item.source_url}"]
    return "\n".join(lines)


async def apply_item(
    db: AsyncSession,
    item: QueueItem,
    *,
    repo_root: Path,
    current_nodes: dict[str, dict],
    dry_run: bool = True,
    reload_data: Callable[[], bool] | None = None,
    plan: ApplyPlan | None = None,
) -> ApplyOutcome:
    """항목 하나를 발행한다. 커밋은 호출자가 한다.

    `plan` 이 주어지면 **재사용한다** — 발행 재시도는 AI 를 다시 부르지 않고 저장된
    계획으로 다시 시도한다(DEC-012 D5).
    """
    if plan is None:
        actions = build_actions(
            await approved_payloads(db, item.id),
            repo_root=repo_root,
            source_key=item.normalized_url,
        )
        plan = ApplyPlan(item_id=item.id, file_actions=[a.as_dict() for a in actions])
        db.add(plan)
        await db.flush()
    else:
        actions = [FileAction(**{k: v for k, v in a.items()}) for a in plan.file_actions]

    violations = validate_plan(actions, repo_root=repo_root, known_stems=set(current_nodes))
    if not violations:
        # 파일 검증을 통과한 것만 그래프에 얹어 본다 — 경로가 틀린 것을 그래프에
        # 넣으면 엉뚱한 위반이 무더기로 나와 진짜 원인이 묻힌다.
        violations = check_graph(current_nodes, actions)

    if violations:
        plan.validation_status = "rejected"
        payload = [v.as_dict() for v in violations]
        result = ApplyResult(
            plan_id=plan.id,
            item_id=item.id,
            status="rejected",
            violations=payload,
            error_code="VALIDATION_REJECTED",
            error_message=f"검증 위반 {len(payload)}건 — 파일을 쓰지 않았다",
        )
        db.add(result)
        item.status = "publish_failed"
        await db.flush()
        logger.warning("발행 거부 item=%s 위반=%d", item.id, len(payload))
        return ApplyOutcome(
            status="rejected",
            result_id=result.id,
            violations=payload,
            error_code="VALIDATION_REJECTED",
        )

    plan.validation_status = "passed"
    item.status = "publishing"
    await db.flush()

    before = head_ref(repo_root)
    try:
        _write_all(repo_root, actions)
    except OSError as exc:
        rollback(repo_root, before)
        return await _fail(db, plan, item, "WRITE_FAILED", str(exc)[:500])

    outcome: PublishOutcome = publish_atomic(
        [a.path for a in actions],
        commit_message(item, actions),
        repo_root=repo_root,
        dry_run=dry_run,
    )
    if not outcome.ok:
        return await _fail(
            db, plan, item, outcome.error_code or "PUBLISH_FAILED", outcome.error_message or ""
        )

    result = ApplyResult(
        plan_id=plan.id, item_id=item.id, status="succeeded", commit_ref=outcome.commit_ref
    )
    db.add(result)
    item.status = "published"
    item.commit_ref = outcome.commit_ref
    from datetime import datetime, timezone

    item.published_at = datetime.now(timezone.utc)
    await db.flush()

    if reload_data is not None:
        # reload 는 발행의 일부가 아니다 — 실패해도 되돌리지 않는다.
        # 이미 origin 에 나갔고, 서버 메모리는 다음 부팅이나 webhook 이 맞춘다.
        try:
            reload_data()
        except Exception:  # noqa: BLE001
            logger.warning("발행 후 reload 실패 (발행은 유효) item=%s", item.id, exc_info=True)

    logger.info("발행 완료 item=%s commit=%s", item.id, outcome.commit_ref)
    return ApplyOutcome(
        status="succeeded", result_id=result.id, commit_ref=outcome.commit_ref
    )


async def _fail(
    db: AsyncSession,
    plan: ApplyPlan,
    item: QueueItem,
    code: str,
    message: str,
) -> ApplyOutcome:
    result = ApplyResult(
        plan_id=plan.id,
        item_id=item.id,
        status="failed",
        error_code=code,
        error_message=message,
    )
    db.add(result)
    # 게이트 승인 상태는 유지한다 — 재시도는 AI 를 다시 부르지 않고 계획만 다시 쓴다.
    item.status = "publish_failed"
    await db.flush()
    return ApplyOutcome(
        status="failed", result_id=result.id, error_code=code, error_message=message
    )


async def latest_plan(db: AsyncSession, item_id: int) -> ApplyPlan | None:
    return await db.scalar(
        select(ApplyPlan)
        .where(ApplyPlan.item_id == item_id)
        .order_by(ApplyPlan.id.desc())
        .limit(1)
    )
