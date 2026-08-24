"""콘텐츠(content) — 1층. 영상 + 교안. 전부 어드민 뒤다.

- GET    /api/admin/contents      — 목록. published_on DESC NULLS LAST
- POST   /api/admin/contents      — 등록. detail_path 원장 md 없으면 422, slug 중복 409
- PATCH  /api/admin/contents/{id} — 부분 수정. 보낸 필드만. detail_path 변경도 같은 검사
- DELETE /api/admin/contents/{id} — 삭제
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.content import (
    AdminContentItem,
    AdminContentsResponse,
    ContentCreate,
    ContentUpdate,
)
from service.content_service import content_service

admin_router = APIRouter(
    prefix="/api/admin/contents",
    tags=["content"],
    dependencies=[Depends(require_admin)],
)


@admin_router.get("", response_model=AdminContentsResponse, response_model_by_alias=True)
async def list_contents(db: AsyncSession = Depends(get_db)) -> AdminContentsResponse:
    dtos = await content_service.list_contents(db)
    return AdminContentsResponse(items=[AdminContentItem.from_dto(d) for d in dtos])


@admin_router.post(
    "", response_model=AdminContentItem, response_model_by_alias=True, status_code=201
)
async def create_content(
    body: ContentCreate, db: AsyncSession = Depends(get_db)
) -> AdminContentItem:
    dto = await content_service.create(db, body.model_dump())
    return AdminContentItem.from_dto(dto)


@admin_router.patch(
    "/{content_id}", response_model=AdminContentItem, response_model_by_alias=True
)
async def patch_content(
    content_id: int, body: ContentUpdate, db: AsyncSession = Depends(get_db)
) -> AdminContentItem:
    dto = await content_service.update(
        db, content_id, body.model_dump(exclude_unset=True)
    )
    return AdminContentItem.from_dto(dto)


@admin_router.delete("/{content_id}")
async def delete_content(content_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    await content_service.delete(db, content_id)
    return {"ok": True}
