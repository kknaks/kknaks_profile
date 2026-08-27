"""회사 — 1층. 전부 어드민 뒤다 — 공개 표면은 /career 상세가 서면 그때 뚫는다.

- GET    /api/admin/companies      — 목록 + career 파생값(역할 수·기간)
- POST   /api/admin/companies      — 등록
- PATCH  /api/admin/companies/{id} — 부분 수정. 보낸 필드만
- DELETE /api/admin/companies/{id} — 역할이 붙어 있으면 409
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.company import (
    AdminCompaniesResponse,
    AdminCompanyItem,
    CompanyCreate,
    CompanyOut,
    CompanyUpdate,
)
from service.company_service import company_service

admin_router = APIRouter(
    prefix="/api/admin/companies",
    tags=["company"],
    dependencies=[Depends(require_admin)],
)


@admin_router.get("", response_model=AdminCompaniesResponse, response_model_by_alias=True)
async def list_companies(db: AsyncSession = Depends(get_db)) -> AdminCompaniesResponse:
    stats = await company_service.list_companies(db)
    return AdminCompaniesResponse(items=[AdminCompanyItem.from_stats(s) for s in stats])


@admin_router.post("", response_model=CompanyOut, response_model_by_alias=True, status_code=201)
async def create_company(
    body: CompanyCreate, db: AsyncSession = Depends(get_db)
) -> CompanyOut:
    dto = await company_service.create(db, body.model_dump())
    return CompanyOut.from_dto(dto)


@admin_router.patch("/{company_id}", response_model=CompanyOut, response_model_by_alias=True)
async def patch_company(
    company_id: int, body: CompanyUpdate, db: AsyncSession = Depends(get_db)
) -> CompanyOut:
    dto = await company_service.update(
        db, company_id, body.model_dump(exclude_unset=True)
    )
    return CompanyOut.from_dto(dto)


@admin_router.delete("/{company_id}")
async def delete_company(company_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    await company_service.delete(db, company_id)
    return {"ok": True}
