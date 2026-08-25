"""GitHub 조회 — 1층. 레포 연결 모달의 owner 후보 · 레포 목록.

- GET /api/admin/github/owners?product_id=N | ?project_id=N — 폼 스코프의 owner 후보
- GET /api/admin/github/repos?owner=X&token_id=N            — 그 owner 의 레포(최근 갱신순)

읽기 전용 — 저장은 기존 POST /api/admin/repos 가 한다. GitHub 실패는 422 메시지.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.github import (
    GithubOwnerItem,
    GithubOwnersResponse,
    GithubRepoItem,
    GithubReposResponse,
)
from service.github_service import github_service

admin_router = APIRouter(
    prefix="/api/admin/github",
    tags=["github"],
    dependencies=[Depends(require_admin)],
)


@admin_router.get(
    "/owners", response_model=GithubOwnersResponse, response_model_by_alias=True
)
async def list_owners(
    product_id: int | None = None,
    project_id: int | None = None,
    db: AsyncSession = Depends(get_db),
) -> GithubOwnersResponse:
    dtos = await github_service.list_owners(db, product_id, project_id)
    return GithubOwnersResponse(items=[GithubOwnerItem.from_dto(d) for d in dtos])


@admin_router.get(
    "/repos", response_model=GithubReposResponse, response_model_by_alias=True
)
async def list_repos(
    owner: str,
    token_id: int | None = None,
    db: AsyncSession = Depends(get_db),
) -> GithubReposResponse:
    dtos = await github_service.list_repos(db, owner, token_id)
    return GithubReposResponse(items=[GithubRepoItem.from_dto(d) for d in dtos])
