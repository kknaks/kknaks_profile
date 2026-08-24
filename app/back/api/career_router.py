"""역할(career) — 1층. 전부 어드민 뒤다 — 공개 표면은 /career 가 서면 그때 뚫는다.

- GET    /api/admin/careers      — 목록. started_on DESC, 회사 이름·파생값 포함
- POST   /api/admin/careers      — 등록. profile_id 는 서버가 첫 profile 로 채운다
- PATCH  /api/admin/careers/{id} — 부분 수정. 보낸 필드만
- DELETE /api/admin/careers/{id} — 삭제
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.career import (
    AdminCareerItem,
    AdminCareersResponse,
    CareerCreate,
    CareerUpdate,
)
from service.career_service import career_service

admin_router = APIRouter(
    prefix="/api/admin/careers",
    tags=["career"],
    dependencies=[Depends(require_admin)],
)


@admin_router.get("", response_model=AdminCareersResponse, response_model_by_alias=True)
async def list_careers(db: AsyncSession = Depends(get_db)) -> AdminCareersResponse:
    dtos = await career_service.list_careers(db)
    return AdminCareersResponse(items=[AdminCareerItem.from_dto(d) for d in dtos])


@admin_router.post(
    "", response_model=AdminCareerItem, response_model_by_alias=True, status_code=201
)
async def create_career(
    body: CareerCreate, db: AsyncSession = Depends(get_db)
) -> AdminCareerItem:
    dto = await career_service.create(db, body.model_dump())
    return AdminCareerItem.from_dto(dto)


@admin_router.patch(
    "/{career_id}", response_model=AdminCareerItem, response_model_by_alias=True
)
async def patch_career(
    career_id: int, body: CareerUpdate, db: AsyncSession = Depends(get_db)
) -> AdminCareerItem:
    dto = await career_service.update(
        db, career_id, body.model_dump(exclude_unset=True)
    )
    return AdminCareerItem.from_dto(dto)


@admin_router.delete("/{career_id}")
async def delete_career(career_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    await career_service.delete(db, career_id)
    return {"ok": True}
