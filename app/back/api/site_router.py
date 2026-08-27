"""사이트 문구 — 1층.

- GET   /api/site                    — 공개 조회. home 히어로 · /about 문구 · footer 가 읽는다
- GET   /api/admin/site-config       — 어드민 목록. 행 그대로 (key · value · note)
- PATCH /api/admin/site-config/{key} — 어드민 수정. value·note 만, 보낸 필드만
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.site import (
    AdminSiteConfigResponse,
    SiteConfigItem,
    SiteConfigUpdate,
    SiteResponse,
)
from service.site_service import site_service

router = APIRouter(prefix="/api/site", tags=["site"])
admin_router = APIRouter(
    prefix="/api/admin/site-config",
    tags=["site"],
    dependencies=[Depends(require_admin)],
)


@router.get("", response_model=SiteResponse)
async def get_site(db: AsyncSession = Depends(get_db)) -> SiteResponse:
    return SiteResponse.from_dtos(await site_service.get_all(db))


@admin_router.get("", response_model=AdminSiteConfigResponse)
async def list_site_config(db: AsyncSession = Depends(get_db)) -> AdminSiteConfigResponse:
    return AdminSiteConfigResponse.from_dtos(await site_service.get_all(db))


@admin_router.patch("/{key}", response_model=SiteConfigItem)
async def patch_site_config(
    key: str, body: SiteConfigUpdate, db: AsyncSession = Depends(get_db)
) -> SiteConfigItem:
    # key 는 경로로만 받는다 — 바꿀 수 없다. 없는 key 는 service 가 404 를 낸다.
    dto = await site_service.update(db, key, body.model_dump(exclude_unset=True))
    return SiteConfigItem(key=dto.key, value=dto.value, note=dto.note)
