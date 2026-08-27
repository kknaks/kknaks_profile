"""레포(repo) — 1층. 커밋을 긁을 레포의 어드민 CRUD + 수집 트리거.

- GET    /api/admin/repos          — 목록. 부모 이름·last_fetched_at·last_error 포함
- POST   /api/admin/repos          — 등록. product/project 둘 중 정확히 하나에 연결
- PATCH  /api/admin/repos/{id}     — 부분 수정. 보낸 필드만
- DELETE /api/admin/repos/{id}     — 삭제(커밋 CASCADE). 권장은 enabled=false
- POST   /api/admin/repos/collect  — 「지금 수집」— 백그라운드로 걸고 즉시 202

공개 라우터 없음 — 잔디 표면은 GET /api/activity (파생) 가 이미 맡는다.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.repo import AdminRepoItem, AdminReposResponse, RepoCreate, RepoUpdate
from service.collect_service import collect_service
from service.repo_service import repo_service

admin_router = APIRouter(
    prefix="/api/admin/repos",
    tags=["repo"],
    dependencies=[Depends(require_admin)],
)


@admin_router.get("", response_model=AdminReposResponse, response_model_by_alias=True)
async def list_repos(db: AsyncSession = Depends(get_db)) -> AdminReposResponse:
    dtos = await repo_service.list_repos(db)
    return AdminReposResponse(items=[AdminRepoItem.from_dto(d) for d in dtos])


@admin_router.post(
    "", response_model=AdminRepoItem, response_model_by_alias=True, status_code=201
)
async def create_repo(
    body: RepoCreate, db: AsyncSession = Depends(get_db)
) -> AdminRepoItem:
    dto = await repo_service.create(db, body.model_dump())
    return AdminRepoItem.from_dto(dto)


@admin_router.post("/collect", status_code=202)
async def collect_now() -> dict:
    """전체 수집을 백그라운드로 걸고 바로 돌아온다 — 결과는 목록 재조회로 본다."""
    started = collect_service.start()
    return {"ok": True, "started": started}  # started=false — 이미 돌고 있다


@admin_router.patch(
    "/{repo_id}", response_model=AdminRepoItem, response_model_by_alias=True
)
async def patch_repo(
    repo_id: int, body: RepoUpdate, db: AsyncSession = Depends(get_db)
) -> AdminRepoItem:
    dto = await repo_service.update(db, repo_id, body.model_dump(exclude_unset=True))
    return AdminRepoItem.from_dto(dto)


@admin_router.delete("/{repo_id}")
async def delete_repo(repo_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    await repo_service.delete(db, repo_id)
    return {"ok": True}
