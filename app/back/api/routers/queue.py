"""승인 큐 API — admin 전용 (KDEV-WORK-014 P2 / KDEV-SPEC-007 §4).

큐 표면 **전체**가 admin 뒤에 있다. 승인 전 초안이 여기 있고, 그것이 공개되면
"승인 전에는 아무것도 내보내지 않는다"는 전제가 무너진다.

발행 관련 엔드포인트(발행 재시도)는 여기 없다 — Apply Executor 가 생기는
WORK-015 소관이다. 없는 기능을 자리만 잡아 두지 않는다.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

import config
from api.routers.auth import require_admin
from core.db import get_db
from core.models import AITask, Gate, GateFeedback, GateRevision, ItemPreparation, QueueItem
from service.pipeline import gates as gates_service
from service.pipeline import intake, prepare_and_open_gate
from service.pipeline.gates import GateError
from service.pipeline.prepare import PREPARABLE_STATUSES
from service.pipeline.route import allowed_groups, route_outcome, validate_route_result

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
    """화면이 선택지를 만들 때 쓰는 값들.

    `reference` group 을 자유 입력으로 두면 사람이 오타를 내고 승인 시점에야 422 를
    본다. 선택지를 서버가 주는 편이 낫다 — `persona/_meta.yaml` 이 SoT 이므로
    프론트에 목록을 복사해 두지 않는다.
    """
    from service.pipeline.definitions import PIPELINES

    return {
        "reference_groups": sorted(allowed_groups(config.repo_root())),
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
    }


@router.patch("/items/{item_id}")
async def update_note(item_id: int, body: UpdateNoteRequest, db: AsyncSession = Depends(get_db)):
    item = await _get_live_item(db, item_id)
    item.note = (body.note or "").strip() or None
    await db.commit()
    return _item_summary(item)


@router.post("/items/{item_id}/prepare")
async def retry_prepare(item_id: int, db: AsyncSession = Depends(get_db)):
    """준비 재시도. 기존 실행 기록은 덮어쓰지 않고 새 버전이 쌓인다."""
    item = await _get_live_item(db, item_id)
    if item.status not in PREPARABLE_STATUSES:
        raise HTTPException(
            status_code=409,
            detail={"code": "PREPARE_RETRY_NOT_ALLOWED", "status": item.status},
        )

    from service.knowledge_capture.source import fetch_source

    summarizer = _summarizer_factory()
    if summarizer is None:
        raise HTTPException(
            status_code=503,
            detail={"code": "SUMMARIZER_UNAVAILABLE", "message": "AI 실행 경로가 준비되지 않았다"},
        )
    # 준비만 하고 끝내면 재시도로 살아난 항목에는 게이트가 영영 안 열린다.
    result = await prepare_and_open_gate(
        db,
        item_id,
        fetch=fetch_source,
        summarize=summarizer,
        generator=_generator_for("route"),
    )
    await db.commit()
    return {
        "status": result.status,
        "version": result.version,
        "error_code": result.error_code,
        "error_message": result.error_message,
    }


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
    await _get_live_item(db, item_id)
    gates = (
        await db.scalars(select(Gate).where(Gate.item_id == item_id).order_by(Gate.stage_no))
    ).all()
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
    generator = _generator_for(gate.stage_name)
    if generator is None:
        raise HTTPException(
            status_code=503,
            detail={"code": "GENERATOR_UNAVAILABLE", "stage": gate.stage_name},
        )
    try:
        revision = await gates_service.regenerate(db, gate, item=item, generator=generator)
    except GateError as exc:
        raise _gate_error(exc) from exc
    await db.commit()
    return {"gate_status": gate.status, "revision": _revision_view(revision)}


@router.post("/gates/{gate_id}/retry")
async def gate_retry(gate_id: int, db: AsyncSession = Depends(get_db)):
    gate, item = await _get_gate(db, gate_id)
    generator = _generator_for(gate.stage_name)
    if generator is None:
        raise HTTPException(
            status_code=503,
            detail={"code": "GENERATOR_UNAVAILABLE", "stage": gate.stage_name},
        )
    try:
        revision = await gates_service.retry(db, gate, item=item, generator=generator)
    except GateError as exc:
        raise _gate_error(exc) from exc
    await db.commit()
    return {"gate_status": gate.status, "revision": _revision_view(revision)}


@router.post("/gates/{gate_id}/approve")
async def gate_approve(gate_id: int, body: ApproveRequest, db: AsyncSession = Depends(get_db)):
    """승인. route 게이트는 여기서 **체인 길이가 확정된다**.

    뒤 스테이지 게이트 생성과 발행은 WORK-015 다 — 지금은 목적지 확정까지다.
    """
    gate, item = await _get_gate(db, gate_id)
    payload = body.payload

    if gate.stage_name == "route" and payload is not None:
        # 사람이 고친 값도 AI 출력과 같은 검사를 통과해야 한다 —
        # 토글을 이상하게 조합한 채로 확정되면 뒤 스테이지가 헛돈다.
        try:
            payload = validate_route_result(payload, groups=allowed_groups(config.repo_root()))
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
    if gate.stage_name == "route":
        outcome = route_outcome(revision.payload or {})
        if outcome == "discarded":
            # 폐기 승인은 항목을 끝낸다. 파일은 만들어지지 않는다.
            item.status = "discarded"
    await db.commit()
    return {
        "gate_status": gate.status,
        "item_status": item.status,
        "route_outcome": outcome,
        "revision": _revision_view(revision),
    }


def _generator_for(stage_name: str):
    from service.pipeline.runtime import current_route_proposer

    if stage_name == "route":
        return current_route_proposer()
    # source_note·concept·derived 는 WORK-015 — 없는 것을 있는 척하지 않는다.
    return None


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
