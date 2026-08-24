"""프로필 — 1층.

- GET   /api/profile       — 공개 조회. /about · home 히어로 · 어드민 기본 정보가 읽는다
- PATCH /api/admin/profile — 어드민 부분 수정. 보낸 필드만 반영한다
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.profile import ProfileOut, ProfileResponse, ProfileUpdate
from service.profile_service import profile_service

router = APIRouter(prefix="/api/profile", tags=["profile"])
admin_router = APIRouter(
    prefix="/api/admin/profile",
    tags=["profile"],
    dependencies=[Depends(require_admin)],
)


@router.get("", response_model=ProfileResponse, response_model_by_alias=True)
async def get_profile(db: AsyncSession = Depends(get_db)) -> ProfileResponse:
    dto = await profile_service.get_profile(db)
    return ProfileResponse(profile=ProfileOut.from_dto(dto))


@admin_router.patch("", response_model=ProfileResponse, response_model_by_alias=True)
async def patch_profile(
    body: ProfileUpdate, db: AsyncSession = Depends(get_db)
) -> ProfileResponse:
    # exclude_unset — 안 보낸 필드는 dict 에 아예 없다. null 을 보낸 것과 다르다.
    dto = await profile_service.update_profile(
        db, body.model_dump(exclude_unset=True)
    )
    return ProfileResponse(profile=ProfileOut.from_dto(dto))
