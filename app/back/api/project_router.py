"""개인 프로젝트(project) — 1층.

- GET    /api/projects            — 공개. visible=true 목록 + 메타(totalCount·categories).
                                    각 항목에 detail_path md 전문(body) — 상세 페이지가
                                    별도 API 없이 이걸 쓴다
- GET    /api/admin/projects      — 목록. started_on DESC NULLS LAST
- POST   /api/admin/projects      — 등록. slug 디렉토리 없으면 422(케이스 2), 중복 409
- PATCH  /api/admin/projects/{id} — 부분 수정. 보낸 필드만. slug 변경도 디렉토리 검사
- DELETE /api/admin/projects/{id} — 삭제
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.project import (
    AdminProjectItem,
    AdminProjectsResponse,
    ProjectCreate,
    ProjectUpdate,
    PublicProjectsResponse,
)
from service.project_service import project_service

router = APIRouter(prefix="/api/projects", tags=["project"])
admin_router = APIRouter(
    prefix="/api/admin/projects",
    tags=["project"],
    dependencies=[Depends(require_admin)],
)


@router.get("", response_model=PublicProjectsResponse, response_model_by_alias=True)
async def get_projects(db: AsyncSession = Depends(get_db)) -> PublicProjectsResponse:
    projects = await project_service.get_public(db)
    return PublicProjectsResponse.from_public(projects)


@admin_router.get("", response_model=AdminProjectsResponse, response_model_by_alias=True)
async def list_projects(db: AsyncSession = Depends(get_db)) -> AdminProjectsResponse:
    dtos = await project_service.list_projects(db)
    return AdminProjectsResponse(items=[AdminProjectItem.from_dto(d) for d in dtos])


@admin_router.post(
    "", response_model=AdminProjectItem, response_model_by_alias=True, status_code=201
)
async def create_project(
    body: ProjectCreate, db: AsyncSession = Depends(get_db)
) -> AdminProjectItem:
    dto = await project_service.create(db, body.model_dump())
    return AdminProjectItem.from_dto(dto)


@admin_router.patch(
    "/{project_id}", response_model=AdminProjectItem, response_model_by_alias=True
)
async def patch_project(
    project_id: int, body: ProjectUpdate, db: AsyncSession = Depends(get_db)
) -> AdminProjectItem:
    dto = await project_service.update(
        db, project_id, body.model_dump(exclude_unset=True)
    )
    return AdminProjectItem.from_dto(dto)


@admin_router.delete("/{project_id}")
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    await project_service.delete(db, project_id)
    return {"ok": True}
