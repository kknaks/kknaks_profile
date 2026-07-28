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

from api.routers.auth import require_admin
from core.db import get_db
from core.models import AITask, ItemPreparation, QueueItem
from service.pipeline import intake, prepare_item
from service.pipeline.prepare import PREPARABLE_STATUSES

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
    result = await prepare_item(db, item_id, fetch=fetch_source, summarize=summarizer)
    await db.commit()
    return {
        "status": result.status,
        "version": result.version,
        "error_code": result.error_code,
        "error_message": result.error_message,
    }


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
