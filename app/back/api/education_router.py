"""교육(education) — 1층. 전부 어드민 뒤다 — 공개 표면은 /career 가 서면 그때 뚫는다.

- GET    /api/admin/education      — 목록. started_on DESC, 파생값 포함
- POST   /api/admin/education      — 등록. profile_id 는 서버가 첫 profile 로 채운다
- PATCH  /api/admin/education/{id} — 부분 수정. 보낸 필드만
- DELETE /api/admin/education/{id} — 삭제. 가드 없음 — education 엔 아무것도 안 붙는다
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.education import (
    AdminEducationItem,
    AdminEducationsResponse,
    EducationCreate,
    EducationUpdate,
)
from service.education_service import education_service

admin_router = APIRouter(
    prefix="/api/admin/education",
    tags=["education"],
    dependencies=[Depends(require_admin)],
)


@admin_router.get("", response_model=AdminEducationsResponse, response_model_by_alias=True)
async def list_educations(db: AsyncSession = Depends(get_db)) -> AdminEducationsResponse:
    dtos = await education_service.list_educations(db)
    return AdminEducationsResponse(items=[AdminEducationItem.from_dto(d) for d in dtos])


@admin_router.post(
    "", response_model=AdminEducationItem, response_model_by_alias=True, status_code=201
)
async def create_education(
    body: EducationCreate, db: AsyncSession = Depends(get_db)
) -> AdminEducationItem:
    dto = await education_service.create(db, body.model_dump())
    return AdminEducationItem.from_dto(dto)


@admin_router.patch(
    "/{education_id}", response_model=AdminEducationItem, response_model_by_alias=True
)
async def patch_education(
    education_id: int, body: EducationUpdate, db: AsyncSession = Depends(get_db)
) -> AdminEducationItem:
    dto = await education_service.update(
        db, education_id, body.model_dump(exclude_unset=True)
    )
    return AdminEducationItem.from_dto(dto)


@admin_router.delete("/{education_id}")
async def delete_education(
    education_id: int, db: AsyncSession = Depends(get_db)
) -> dict:
    await education_service.delete(db, education_id)
    return {"ok": True}
