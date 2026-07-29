"""승인 큐 API — admin 전용 (KDEV-WORK-014 P2 / KDEV-SPEC-007 §4).

큐 표면 **전체**가 admin 뒤에 있다. 승인 전 초안이 여기 있고, 그것이 공개되면
"승인 전에는 아무것도 내보내지 않는다"는 전제가 무너진다.

발행 관련 엔드포인트(발행 재시도)는 여기 없다 — Apply Executor 가 생기는
WORK-015 소관이다. 없는 기능을 자리만 잡아 두지 않는다.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

import config
from api.routers.auth import require_admin
from core.db import get_db
from core.models import (
    AITask,
    ApplyResult,
    Gate,
    GateFeedback,
    GateRevision,
    ItemPreparation,
    QueueItem,
)
from service.pipeline import chain
from service.pipeline import gates as gates_service
from service.pipeline import harvest_preparation, intake
from service.pipeline.gates import GateError
from service.pipeline.prepare import PREPARABLE_STATUSES
from service.pipeline.route import route_outcome, validate_route_result
from service.pipeline.stages.concept import apply_exclusions

logger = logging.getLogger("kknaks-back.queue-api")

router = APIRouter(prefix="/api/admin/queue", tags=["queue"], dependencies=[Depends(require_admin)])

#: 기본 목록에서 감추는 상태 — 끝난 항목이 검토 대기와 섞이면 할 일이 안 보인다.
HIDDEN_STATUSES = ("published", "discarded", "deleted")


class CreateItemRequest(BaseModel):
    source_url: str | None = Field(default=None, max_length=2000)
    note: str | None = Field(default=None, max_length=20000)
    source_kind: str | None = Field(default=None, max_length=32)
    #: "이미 발행된 자료지만 새로 정리하겠다" 는 사람의 결정.
    allow_republish: bool = False


class UpdateNoteRequest(BaseModel):
    note: str | None = Field(default=None, max_length=20000)


def _item_summary(item: QueueItem) -> dict[str, Any]:
    return {
        "id": item.id,
        "source_kind": item.source_kind,
        "source_url": item.source_url,
        "note": item.note,
        "channel": item.channel,
        "status": item.status,
        "submitted_by": item.submitted_by,
        "submitted_at": item.submitted_at.isoformat() if item.submitted_at else None,
        "published_at": item.published_at.isoformat() if item.published_at else None,
        "commit_ref": item.commit_ref,
    }


async def _get_live_item(db: AsyncSession, item_id: int) -> QueueItem:
    item = await db.get(QueueItem, item_id)
    if item is None or item.deleted_at is not None:
        raise HTTPException(status_code=404, detail="item not found")
    return item


@router.get("/meta")
async def queue_meta():
    """화면이 쓰는 파이프라인 정의. 정의가 코드에 있으므로 프론트에 복사해 두지 않는다."""
    from service.pipeline.definitions import PIPELINES

    return {
        "pipelines": {
            kind: [
                {"name": s.name, "kind": s.kind, "optional": s.optional}
                for s in pipeline.stages
            ]
            for kind, pipeline in PIPELINES.items()
        },
    }


@router.post("/items", status_code=201)
async def create_item(body: CreateItemRequest, db: AsyncSession = Depends(get_db)):
    if body.source_url is None and not (body.note or "").strip():
        raise HTTPException(status_code=422, detail="source_url 또는 note 중 하나는 필요하다")

    result = await intake(
        db,
        source_url=body.source_url,
        note=body.note,
        channel="manual",
        source_kind=body.source_kind,
        allow_republish=body.allow_republish,
    )
    await db.commit()

    if result.outcome == "duplicate_published":
        # 막지 않고 알린다 — 같은 자료의 재정리가 정당한 경우가 있다(S-4).
        raise HTTPException(
            status_code=409,
            detail={
                "code": "DUPLICATE_PUBLISHED",
                "existing_item_id": result.existing_item_id,
            },
        )
    if result.item_id is not None:
        await _follow(result.item_id)
    return {"outcome": result.outcome, "item_id": result.item_id}


@router.get("/items")
async def list_items(
    db: AsyncSession = Depends(get_db),
    status: str | None = Query(default=None),
    include_done: bool = Query(default=False),
    limit: int = Query(default=100, ge=1, le=500),
):
    stmt = select(QueueItem).where(QueueItem.deleted_at.is_(None))
    if status:
        stmt = stmt.where(QueueItem.status == status)
    elif not include_done:
        stmt = stmt.where(QueueItem.status.not_in(HIDDEN_STATUSES))
    stmt = stmt.order_by(desc(QueueItem.submitted_at)).limit(limit)

    items = (await db.scalars(stmt)).all()
    # 목록도 수확 지점이다 — 준비 중 항목은 여기서 검토 대기로 넘어간다.
    # 하나가 넘어갔다고 멈추지 않는다. 모두 봐야 한다.
    harvested = False
    for item in items:
        harvested |= await _harvest_item(db, item)
    if harvested:
        await db.commit()

    counts = dict(
        (
            await db.execute(
                select(QueueItem.status, func.count())
                .where(QueueItem.deleted_at.is_(None))
                .group_by(QueueItem.status)
            )
        ).all()
    )
    return {"items": [_item_summary(i) for i in items], "counts": counts}


@router.get("/items/{item_id}")
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await _get_live_item(db, item_id)
    if await _harvest_item(db, item):
        await db.commit()

    preparations = (
        await db.scalars(
            select(ItemPreparation)
            .where(ItemPreparation.item_id == item_id)
            .order_by(ItemPreparation.version)
        )
    ).all()
    tasks = (
        await db.scalars(select(AITask).where(AITask.item_id == item_id).order_by(AITask.id))
    ).all()
    # 발행 결과도 준다 — **거부 사유가 화면에 없으면 재시도 판단이 서지 않는다.**
    # 종전에는 항목이 `발행 실패` 로만 보이고 무엇이 막았는지는 DB 를 봐야 알 수 있었다.
    applies = (
        await db.scalars(
            select(ApplyResult).where(ApplyResult.item_id == item_id).order_by(ApplyResult.id)
        )
    ).all()
    return {
        **_item_summary(item),
        "preparations": [
            {
                "id": p.id,
                "version": p.version,
                "status": p.status,
                "payload": p.payload,
                "created_at": p.created_at.isoformat() if p.created_at else None,
            }
            for p in preparations
        ],
        # 실패한 실행도 그대로 보여준다 — 왜 막혔는지가 재시도 판단의 근거다.
        "ai_tasks": [
            {
                "id": t.id,
                "kind": t.kind,
                "status": t.status,
                "retry_of_task_id": t.retry_of_task_id,
                "error_code": t.error_code,
                "error_message": t.error_message,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in tasks
        ],
        "apply_results": [
            {
                "id": a.id,
                "status": a.status,
                "commit_ref": a.commit_ref,
                "violations": a.violations,
                "error_code": a.error_code,
                "error_message": a.error_message,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in applies
        ],
    }


@router.patch("/items/{item_id}")
async def update_note(item_id: int, body: UpdateNoteRequest, db: AsyncSession = Depends(get_db)):
    item = await _get_live_item(db, item_id)
    item.note = (body.note or "").strip() or None
    await db.commit()
    return _item_summary(item)


@router.post("/items/{item_id}/prepare")
async def retry_prepare(item_id: int, db: AsyncSession = Depends(get_db)):
    """준비 재시도 — **다시 대기줄에 세운다** (KDEV-WORK-016).

    수집도 요약도 여기서 하지 않는다. 수집만 해도 최대 15초라 그만큼 응답이 늦고,
    그 사이 프록시가 끊으면 트랜잭션이 롤백돼 재시도한 흔적조차 남지 않는다.
    드라이버가 이어서 수집하고 요약을 제출한다.

    기존 실행 기록은 덮어쓰지 않고 새 버전이 쌓인다.
    """
    item = await _get_live_item(db, item_id)
    if item.status not in PREPARABLE_STATUSES:
        raise HTTPException(
            status_code=409,
            detail={"code": "PREPARE_RETRY_NOT_ALLOWED", "status": item.status},
        )
    if _summarizer_factory() is None:
        # 캡처가 꺼져 있으면 재시도도 불가능한 것이 사실이다. 조용히 대기줄에만
        # 세우면 영영 안 도는 항목이 `received` 로 쌓인다.
        raise HTTPException(
            status_code=503,
            detail={"code": "SUMMARIZER_UNAVAILABLE", "message": "AI 실행 경로가 준비되지 않았다"},
        )

    item.status = "received"
    await db.commit()
    # 커밋 뒤에 넘긴다 — 커밋 전이면 드라이버가 옛 상태를 읽는다.
    await _follow(item_id)
    return {"status": item.status, "version": None, "error_code": None, "error_message": None}


async def _harvest_item(db: AsyncSession, item: QueueItem) -> bool:
    """진행 중인 준비를 수확한다. 바뀌었으면 `True`.

    준비가 끝나면 첫 게이트까지 열린다(제출까지). 실행기에 못 닿아도 조회 자체는
    실패시키지 않는다 — 화면이 통째로 비면 무엇이 진행 중인지도 못 본다.
    """
    if item.status == "received":
        # 읽기 경로에서 수집·요약을 하지 않는다. 드라이버를 다시 깨우기만 한다 —
        # 드라이버가 죽었거나 재시작 사이에 접수된 항목이 여기서 살아난다.
        await _follow(item.id)
        return False
    if item.status != "preparing":
        return False
    summarizer = _summarizer_factory()
    if summarizer is None:
        # 수확할 방법이 없다. 상태를 지어내지 않고 그대로 둔다 —
        # 캡처 런타임이 다시 뜨면 이어서 수확된다.
        return False
    try:
        result = await harvest_preparation(
            db, item, summarize=summarizer, runner=_runner_for("route")
        )
    except Exception:  # noqa: BLE001
        logger.exception("항목 %s 준비 수확 실패 — 조회는 그대로 내려보낸다", item.id)
        return False
    return result.status != "preparing"


class FeedbackRequest(BaseModel):
    body: str = Field(max_length=10000)


class ApproveRequest(BaseModel):
    #: 화면에서 토글을 고친 경우. AI 제안 그대로가 아니라 **사람이 고친 결과**가 승인 대상이다.
    payload: dict[str, Any] | None = None
    #: 낙관적 잠금 — 다른 탭에서 재생성이 돌았는데 옛 화면의 승인이 먹으면
    #: 사람이 보지 않은 내용을 승인하게 된다.
    expected_revision_id: int | None = None


def _revision_view(revision: GateRevision) -> dict[str, Any]:
    return {
        "id": revision.id,
        "version": revision.version,
        "status": revision.status,
        "payload": revision.payload,
        "parent_revision_id": revision.parent_revision_id,
        "feedback_id": revision.feedback_id,
        "created_at": revision.created_at.isoformat() if revision.created_at else None,
    }


async def _gate_view(db: AsyncSession, gate: Gate) -> dict[str, Any]:
    revisions = (
        await db.scalars(
            select(GateRevision)
            .where(GateRevision.gate_id == gate.id)
            .order_by(GateRevision.version)
        )
    ).all()
    feedbacks = (
        await db.scalars(
            select(GateFeedback).where(GateFeedback.gate_id == gate.id).order_by(GateFeedback.id)
        )
    ).all()
    return {
        "id": gate.id,
        "stage_name": gate.stage_name,
        "stage_no": gate.stage_no,
        "status": gate.status,
        "active_revision_id": gate.active_revision_id,
        "approved_revision_id": gate.approved_revision_id,
        # 이전 버전도 그대로 준다 — read-only 로 남는다는 계약이 화면에서 보여야 한다.
        "revisions": [_revision_view(r) for r in revisions],
        "feedbacks": [
            {
                "id": f.id,
                "target_revision_id": f.target_revision_id,
                "body": f.body,
                "status": f.status,
            }
            for f in feedbacks
        ],
    }


async def _get_gate(db: AsyncSession, gate_id: int) -> tuple[Gate, QueueItem]:
    gate = await db.get(Gate, gate_id)
    if gate is None:
        raise HTTPException(status_code=404, detail="gate not found")
    item = await _get_live_item(db, gate.item_id)
    return gate, item


def _gate_error(exc: GateError) -> HTTPException:
    status = 409 if exc.code != "FEEDBACK_TOO_SHORT" else 422
    return HTTPException(status_code=status, detail={"code": exc.code, "message": exc.message})


@router.get("/items/{item_id}/gates")
async def list_gates(item_id: int, db: AsyncSession = Depends(get_db)):
    """게이트 목록 — **조회하면서 수확한다** (KDEV-WORK-016 P1 / SPEC-009).

    실행은 요청 밖에서 돈다. 그 결과를 DB 에 옮기는 것은 화면이 이 목록을 폴링할 때다.
    수확은 멱등이라 폴링이 겹쳐도 revision 이 두 번 채워지지 않는다.

    **준비부터 본다.** 아직 준비 중인 항목은 게이트가 하나도 없고, 그 수확이
    첫 게이트를 연다 — 여기서 건너뛰면 이 화면만 보는 사람은 영영 진행되지 않는다.
    """
    item = await _get_live_item(db, item_id)
    harvested = await _harvest_item(db, item)

    gates = (
        await db.scalars(select(Gate).where(Gate.item_id == item_id).order_by(Gate.stage_no))
    ).all()

    for gate in gates:
        if gate.status not in gates_service.IN_FLIGHT:
            continue
        runner = _runner_for(gate.stage_name)
        if runner is None:
            # 실행기가 없으면 수확할 방법이 없다. 상태를 지어내지 않고 그대로 둔다 —
            # 캡처 런타임이 다시 뜨면 이어서 수확된다.
            continue
        try:
            harvested |= await gates_service.harvest(db, gate, item=item, runner=runner)
        except Exception:  # noqa: BLE001
            # 실행기에 못 닿는다고 **목록 자체가 실패하면 안 된다** — 화면이 통째로
            # 비면 사용자는 무엇이 진행 중인지도 못 본다. 게이트는 진행 중으로 남고
            # 다음 폴링이 다시 시도한다.
            logger.exception("게이트 %s 수확 실패 — 목록은 그대로 내려보낸다", gate.id)
    if harvested:
        await db.commit()

    return {"gates": [await _gate_view(db, g) for g in gates]}


@router.post("/gates/{gate_id}/feedback")
async def gate_feedback(
    gate_id: int, body: FeedbackRequest, db: AsyncSession = Depends(get_db)
):
    gate, _ = await _get_gate(db, gate_id)
    try:
        feedback = await gates_service.submit_feedback(db, gate, body.body)
    except GateError as exc:
        raise _gate_error(exc) from exc
    await db.commit()
    return {"feedback_id": feedback.id, "gate_status": gate.status}


@router.post("/gates/{gate_id}/regenerate")
async def gate_regenerate(gate_id: int, db: AsyncSession = Depends(get_db)):
    gate, item = await _get_gate(db, gate_id)
    runner = _runner_for(gate.stage_name)
    if runner is None:
        raise HTTPException(
            status_code=503,
            detail={"code": "GENERATOR_UNAVAILABLE", "stage": gate.stage_name},
        )
    try:
        revision = await gates_service.regenerate(db, gate, item=item, runner=runner)
    except GateError as exc:
        raise _gate_error(exc) from exc
    await db.commit()
    await _follow(gate.item_id)
    return {"gate_status": gate.status, "revision": _revision_view(revision)}


@router.post("/gates/{gate_id}/retry")
async def gate_retry(gate_id: int, db: AsyncSession = Depends(get_db)):
    gate, item = await _get_gate(db, gate_id)
    runner = _runner_for(gate.stage_name)
    if runner is None:
        raise HTTPException(
            status_code=503,
            detail={"code": "GENERATOR_UNAVAILABLE", "stage": gate.stage_name},
        )
    try:
        revision = await gates_service.retry(db, gate, item=item, runner=runner)
    except GateError as exc:
        raise _gate_error(exc) from exc
    await db.commit()
    await _follow(gate.item_id)
    return {"gate_status": gate.status, "revision": _revision_view(revision)}


@router.post("/items/{item_id}/reopen-route")
async def reopen_route(item_id: int, db: AsyncSession = Depends(get_db)):
    """목적지 재검토 — 유일한 역방향 전이(DEC-011 D5).

    뒤 게이트는 무효화되지만 **기록은 남는다.** 수집·요약은 다시 돌지 않는다.
    """
    item = await _get_live_item(db, item_id)
    runner = _runner_for("route")
    if runner is None:
        raise HTTPException(
            status_code=503, detail={"code": "GENERATOR_UNAVAILABLE", "stage": "route"}
        )
    try:
        gate = await chain.reopen_route(db, item, runner=runner)
    except GateError as exc:
        raise _gate_error(exc) from exc
    await db.commit()
    await _follow(item.id)
    return {"gate_id": gate.id, "gate_status": gate.status, "item_status": item.status}


@router.post("/gates/{gate_id}/approve")
async def gate_approve(gate_id: int, body: ApproveRequest, db: AsyncSession = Depends(get_db)):
    """승인. route 게이트는 여기서 **체인 길이가 확정된다**.

    뒤 스테이지 게이트 생성과 발행은 WORK-015 다 — 지금은 목적지 확정까지다.
    """
    gate, item = await _get_gate(db, gate_id)
    payload = body.payload

    if gate.stage_name == "concept" and payload is not None:
        current = await db.get(GateRevision, gate.active_revision_id)
        try:
            payload = apply_exclusions(payload, (current.payload or {}) if current else {})
        except GateError as exc:
            raise HTTPException(
                status_code=422, detail={"code": exc.code, "message": exc.message}
            ) from exc

    if gate.stage_name == "route" and payload is not None:
        # 사람이 고친 값도 AI 출력과 같은 검사를 통과해야 한다 —
        # 토글을 이상하게 조합한 채로 확정되면 뒤 스테이지가 헛돈다.
        try:
            payload = validate_route_result(payload)
        except GateError as exc:
            raise HTTPException(
                status_code=422, detail={"code": exc.code, "message": exc.message}
            ) from exc

    try:
        revision = await gates_service.approve(
            db, gate, payload_override=payload, expected_revision_id=body.expected_revision_id
        )
    except GateError as exc:
        raise _gate_error(exc) from exc

    outcome = None
    next_gate = None
    if gate.stage_name == "route":
        outcome = route_outcome(revision.payload or {})
        if outcome == "discarded":
            # 폐기 승인은 항목을 끝낸다. 파일은 만들어지지 않는다.
            item.status = "discarded"

    published = None
    advanced = None
    if item.status != "discarded":
        # 중간 승인은 다음 스테이지를 열 뿐 파일을 만들지 않는다(DEC-011 D6).
        advanced = await chain.advance(db, item, gate, runners=_runners())
        next_gate = advanced.gate
        if advanced.chain_complete:
            # 스테이지가 정말 남지 않았을 때만 발행한다. `gate is None` 으로 판단하면
            # **생성기가 없어 못 연 경우까지 발행**되어 미완성 체인이 나간다.
            published = await _publish(db, item)
    await db.commit()
    # 승인이 다음 스테이지를 제출했다. 그 완료를 기다리는 것도 요청이 아니다.
    await _follow(item.id)
    return {
        "gate_status": gate.status,
        "item_status": item.status,
        "route_outcome": outcome,
        "next_stage": advanced.pending_stage if advanced else None,
        "blocked": bool(advanced and advanced.blocked),
        "published": published,
        "revision": _revision_view(revision),
    }


async def _publish(db: AsyncSession, item: QueueItem, *, plan=None) -> dict[str, Any]:
    """발행을 실행하고 화면이 쓸 요약을 돌려준다."""
    from service.apply import apply_item

    def reload_local() -> bool:
        from main import reload_data

        return reload_data()

    outcome = await apply_item(
        db,
        item,
        repo_root=config.repo_root(),
        current_nodes=_current_nodes(),
        dry_run=config.job_git_push_dry_run(),
        reload_data=reload_local,
        plan=plan,
    )
    return {
        "status": outcome.status,
        "commit_ref": outcome.commit_ref,
        "violations": outcome.violations,
        "error_code": outcome.error_code,
        "error_message": outcome.error_message,
    }


def _current_nodes() -> dict[str, dict]:
    """부팅 때 만든 노드 맵. 없으면 빈 맵 — 그래프 검증이 헐거워질 뿐 발행을 막지 않는다."""
    try:
        from main import get_data

        return get_data().get("_nodes") or {}
    except Exception:  # noqa: BLE001
        return {}


@router.post("/items/{item_id}/publish")
async def retry_publish(item_id: int, db: AsyncSession = Depends(get_db)):
    """발행 재시도 — **AI 를 다시 부르지 않는다.**

    저장된 계획으로 다시 쓴다(DEC-012 D5). 게이트 승인 상태는 그대로다.
    """
    item = await _get_live_item(db, item_id)
    if item.status != "publish_failed":
        raise HTTPException(
            status_code=409,
            detail={"code": "PUBLISH_RETRY_NOT_ALLOWED", "status": item.status},
        )
    from service.apply import latest_plan

    plan = await latest_plan(db, item_id)
    result = await _publish(db, item, plan=plan)
    await db.commit()
    return {"item_status": item.status, **result}


async def _follow(item_id: int) -> None:
    from service.pipeline.runtime import follow

    await follow(item_id)


def _runners() -> dict[str, Any]:
    from service.pipeline.runtime import current_runners

    return current_runners()


def _runner_for(stage_name: str):
    return _runners().get(stage_name)


@router.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """soft delete. 행은 남기고 목록에서만 감춘다."""
    item = await _get_live_item(db, item_id)
    if item.status == "publishing":
        # 발행 중 삭제는 커밋이 반쯤 나간 상태를 만든다.
        raise HTTPException(
            status_code=409, detail={"code": "DELETE_WHILE_PUBLISHING"}
        )
    item.status = "deleted"
    item.deleted_at = datetime.now(timezone.utc)
    await db.commit()
    return {"id": item.id, "status": item.status}


def _summarizer_factory():
    """실행 중인 캡처 런타임의 요약기를 빌려 쓴다.

    큐 API 는 자기 broker 를 새로 열지 않는다 — 연결을 두 벌 들고 있으면 어느 쪽이
    살아 있는지 알기 어려워진다. 캡처가 꺼져 있으면 재시도도 불가능한 것이 정직하다.
    """
    from service.pipeline.runtime import current_summarizer

    return current_summarizer()
