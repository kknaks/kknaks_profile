"""해결한 문제(problem) — 1층. 전부 어드민 뒤다 — 이력서의 알맹이라 공개 표면이 없다.

- GET    /api/admin/problems      — 목록. careerTitle·companyName·productTitle 포함
- POST   /api/admin/problems      — 등록. careerId 필수, productId 는 그 역할의 제품만
- PATCH  /api/admin/problems/{id} — 부분 수정. productId: null 은 연결 해제
- DELETE /api/admin/problems/{id} — 삭제
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.problem import (
    AdminProblemItem,
    AdminProblemsResponse,
    ProblemCreate,
    ProblemUpdate,
)
from service.problem_service import problem_service

admin_router = APIRouter(
    prefix="/api/admin/problems",
    tags=["problem"],
    dependencies=[Depends(require_admin)],
)


@admin_router.get("", response_model=AdminProblemsResponse, response_model_by_alias=True)
async def list_problems(db: AsyncSession = Depends(get_db)) -> AdminProblemsResponse:
    dtos = await problem_service.list_problems(db)
    return AdminProblemsResponse(items=[AdminProblemItem.from_dto(d) for d in dtos])


@admin_router.post(
    "", response_model=AdminProblemItem, response_model_by_alias=True, status_code=201
)
async def create_problem(
    body: ProblemCreate, db: AsyncSession = Depends(get_db)
) -> AdminProblemItem:
    dto = await problem_service.create(db, body.model_dump())
    return AdminProblemItem.from_dto(dto)


@admin_router.patch(
    "/{problem_id}", response_model=AdminProblemItem, response_model_by_alias=True
)
async def patch_problem(
    problem_id: int, body: ProblemUpdate, db: AsyncSession = Depends(get_db)
) -> AdminProblemItem:
    dto = await problem_service.update(
        db, problem_id, body.model_dump(exclude_unset=True)
    )
    return AdminProblemItem.from_dto(dto)


@admin_router.delete("/{problem_id}")
async def delete_problem(problem_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    await problem_service.delete(db, problem_id)
    return {"ok": True}
