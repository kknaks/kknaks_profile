"""인박스(queue) — 1층. 캡처 → queue 행 생성 + 목록 + 재시도 (inbox.md Step 1·2·3).

- POST /api/admin/queue            — 행 생성(queued) + 비동기 처리를 건다(Step 3)
- GET  /api/admin/queue            — 최신순 목록 + 상태별 counts
- POST /api/admin/queue/{id}/retry — failed → queued + 처리를 처음부터 다시 건다

처리는 FastAPI BackgroundTasks 로 건다. 백그라운드 태스크가 get_db 의 teardown
commit 보다 먼저 돌 수 있어서(실측), 태스크를 걸기 전에 명시적으로 commit 한다 —
처리기는 자기 세션(SessionLocal)으로 행을 읽는다. teardown 의 commit 은 no-op 이 된다.

삭제 없음(v1) — 잘못 넣었으면 게이트에서 거절한다. 공개 라우터도 없다 —
파이프라인의 기록이지 표면이 아니다(erd §queue).
"""

from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.queue import AdminQueueItem, AdminQueueResponse, QueueCreate
from service.inbox_service import inbox_pipeline
from service.queue_service import queue_service

admin_router = APIRouter(
    prefix="/api/admin/queue",
    tags=["queue"],
    dependencies=[Depends(require_admin)],
)


@admin_router.get("", response_model=AdminQueueResponse, response_model_by_alias=True)
async def list_queue(db: AsyncSession = Depends(get_db)) -> AdminQueueResponse:
    result = await queue_service.list_queue(db)
    return AdminQueueResponse.from_list(result)


@admin_router.post(
    "", response_model=AdminQueueItem, response_model_by_alias=True, status_code=201
)
async def create_queue_item(
    body: QueueCreate,
    background: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> AdminQueueItem:
    dto = await queue_service.create(db, body.kind, body.source_url, body.note)
    await db.commit()  # 처리기가 자기 세션으로 이 행을 읽는다 — 걸기 전에 확정
    background.add_task(inbox_pipeline.process, dto.id)
    return AdminQueueItem.from_dto(dto)


@admin_router.post(
    "/{queue_id}/retry", response_model=AdminQueueItem, response_model_by_alias=True
)
async def retry_queue_item(
    queue_id: int,
    background: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> AdminQueueItem:
    dto = await queue_service.retry(db, queue_id)
    await db.commit()  # 같은 이유 — queued 전이를 확정하고 처리를 건다
    background.add_task(inbox_pipeline.process, dto.id)
    return AdminQueueItem.from_dto(dto)
