"""회사 제품(product) — 1층. 전부 어드민 뒤다 — 공개 표면은 아직 안 정해졌다(erd.md).

- GET    /api/admin/products      — 목록. careerTitle·companyName(2단 조인) 포함
- POST   /api/admin/products      — 등록. careerId 필수, slug UK 중복 409
- PATCH  /api/admin/products/{id} — 부분 수정. 보낸 필드만
- DELETE /api/admin/products/{id} — 삭제
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.product import (
    AdminProductItem,
    AdminProductsResponse,
    ProductCreate,
    ProductUpdate,
)
from service.product_service import product_service

admin_router = APIRouter(
    prefix="/api/admin/products",
    tags=["product"],
    dependencies=[Depends(require_admin)],
)


@admin_router.get("", response_model=AdminProductsResponse, response_model_by_alias=True)
async def list_products(db: AsyncSession = Depends(get_db)) -> AdminProductsResponse:
    dtos = await product_service.list_products(db)
    return AdminProductsResponse(items=[AdminProductItem.from_dto(d) for d in dtos])


@admin_router.post(
    "", response_model=AdminProductItem, response_model_by_alias=True, status_code=201
)
async def create_product(
    body: ProductCreate, db: AsyncSession = Depends(get_db)
) -> AdminProductItem:
    dto = await product_service.create(db, body.model_dump())
    return AdminProductItem.from_dto(dto)


@admin_router.patch(
    "/{product_id}", response_model=AdminProductItem, response_model_by_alias=True
)
async def patch_product(
    product_id: int, body: ProductUpdate, db: AsyncSession = Depends(get_db)
) -> AdminProductItem:
    dto = await product_service.update(
        db, product_id, body.model_dump(exclude_unset=True)
    )
    return AdminProductItem.from_dto(dto)


@admin_router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    await product_service.delete(db, product_id)
    return {"ok": True}
