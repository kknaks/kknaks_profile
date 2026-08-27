"""git_token — 1층. 어드민 설정의 토큰 관리.

- GET    /api/admin/git-tokens        — 목록 (원문·암호문 없음)
- POST   /api/admin/git-tokens        — 등록 {kind, account, email, token, companyId?}
- PUT    /api/admin/git-tokens/{id}   — 토큰 값 교체 {token}
- PATCH  /api/admin/git-tokens/{id}   — 부분 수정 {enabled? · companyId?} — 보낸 필드만
- DELETE /api/admin/git-tokens/{id}   — 삭제 (repo 연결은 SET NULL → 무토큰)
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.git_token import (
    GitTokenCreate,
    GitTokenItem,
    GitTokenPatch,
    GitTokenReplace,
    GitTokensResponse,
)
from service.git_token_service import git_token_service

admin_router = APIRouter(
    prefix="/api/admin/git-tokens",
    tags=["git-token"],
    dependencies=[Depends(require_admin)],
)


@admin_router.get("", response_model=GitTokensResponse, response_model_by_alias=True)
async def list_tokens(db: AsyncSession = Depends(get_db)) -> GitTokensResponse:
    dtos = await git_token_service.list_tokens(db)
    return GitTokensResponse(items=[GitTokenItem.from_dto(d) for d in dtos])


@admin_router.post(
    "", response_model=GitTokenItem, response_model_by_alias=True, status_code=201
)
async def create_token(
    body: GitTokenCreate, db: AsyncSession = Depends(get_db)
) -> GitTokenItem:
    dto = await git_token_service.create(
        db, body.kind, body.account, body.email, body.token, body.company_id
    )
    return GitTokenItem.from_dto(dto)


@admin_router.put("/{token_id}")
async def replace_token(
    token_id: int, body: GitTokenReplace, db: AsyncSession = Depends(get_db)
) -> dict[str, bool]:
    await git_token_service.replace(db, token_id, body.token)
    return {"ok": True}


@admin_router.patch(
    "/{token_id}", response_model=GitTokenItem, response_model_by_alias=True
)
async def patch_token(
    token_id: int, body: GitTokenPatch, db: AsyncSession = Depends(get_db)
) -> GitTokenItem:
    dto = await git_token_service.update(
        db, token_id, body.model_dump(exclude_unset=True)
    )
    return GitTokenItem.from_dto(dto)


@admin_router.delete("/{token_id}")
async def delete_token(token_id: int, db: AsyncSession = Depends(get_db)) -> dict[str, bool]:
    await git_token_service.delete(db, token_id)
    return {"ok": True}
