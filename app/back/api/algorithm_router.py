"""알고리즘(algorithm) — 1층. 전부 어드민 뒤다 — 메타 관리 + today 토글.

- GET    /api/admin/algorithms      — 목록. today 행 맨 앞, 그 뒤 published_on DESC NULLS LAST
- POST   /api/admin/algorithms      — 등록. difficulty 오값·md 부재 422, slug 중복 409
- PATCH  /api/admin/algorithms/{id} — 부분 수정. today=true 면 기존 today 를 먼저 내린다
- DELETE /api/admin/algorithms/{id} — 삭제
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.algorithm import (
    AdminAlgorithmItem,
    AdminAlgorithmsResponse,
    AlgorithmCreate,
    AlgorithmUpdate,
)
from service.algorithm_service import algorithm_service

admin_router = APIRouter(
    prefix="/api/admin/algorithms",
    tags=["algorithm"],
    dependencies=[Depends(require_admin)],
)


@admin_router.get("", response_model=AdminAlgorithmsResponse, response_model_by_alias=True)
async def list_algorithms(db: AsyncSession = Depends(get_db)) -> AdminAlgorithmsResponse:
    dtos = await algorithm_service.list_algorithms(db)
    return AdminAlgorithmsResponse(items=[AdminAlgorithmItem.from_dto(d) for d in dtos])


@admin_router.post(
    "", response_model=AdminAlgorithmItem, response_model_by_alias=True, status_code=201
)
async def create_algorithm(
    body: AlgorithmCreate, db: AsyncSession = Depends(get_db)
) -> AdminAlgorithmItem:
    dto = await algorithm_service.create(db, body.model_dump())
    return AdminAlgorithmItem.from_dto(dto)


@admin_router.patch(
    "/{algorithm_id}", response_model=AdminAlgorithmItem, response_model_by_alias=True
)
async def patch_algorithm(
    algorithm_id: int, body: AlgorithmUpdate, db: AsyncSession = Depends(get_db)
) -> AdminAlgorithmItem:
    dto = await algorithm_service.update(
        db, algorithm_id, body.model_dump(exclude_unset=True)
    )
    return AdminAlgorithmItem.from_dto(dto)


@admin_router.delete("/{algorithm_id}")
async def delete_algorithm(
    algorithm_id: int, db: AsyncSession = Depends(get_db)
) -> dict:
    await algorithm_service.delete(db, algorithm_id)
    return {"ok": True}
