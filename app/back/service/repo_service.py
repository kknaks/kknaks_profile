"""레포(repo) — 2층. 커밋을 긁을 레포의 등록·수정·삭제.

지우는 것보다 enabled=false 를 권장한다 — 커밋이 CASCADE 로 쓸려간다.
그래도 DELETE 는 열어 둔다(발주 확정) — 가드 없이 지운다.
"""

from __future__ import annotations

import re
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import ConflictError, NotFoundError, ValidationError
from dto.repo import RepoDTO
from repository.git_token_repo import GitTokenRepository
from repository.product_repo import ProductRepository
from repository.project_repo import ProjectRepository
from repository.repo_repo import RepoRepository

# GitHub 의 owner/name — 딱 한 번의 / 와 양쪽 비지 않은 조각.
_SLUG_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")



class RepoService:
    def __init__(
        self,
        repo_repo: RepoRepository,
        product_repo: ProductRepository,
        project_repo: ProjectRepository,
        git_token_repo: GitTokenRepository,
    ) -> None:
        self._repo_repo = repo_repo
        self._product_repo = product_repo
        self._project_repo = project_repo
        self._git_token_repo = git_token_repo

    async def list_repos(self, session: AsyncSession) -> list[RepoDTO]:
        return await self._repo_repo.list_with_parent(session)

    def _check_slug(self, slug: str) -> str:
        slug = slug.strip()
        if not _SLUG_RE.match(slug):
            raise ValidationError(f"slug 는 owner/name 형식이어야 합니다: {slug!r}")
        return slug

    async def _check_parent(
        self, session: AsyncSession, product_id: int | None, project_id: int | None
    ) -> None:
        """부모는 둘 중 정확히 하나(DB CHECK ck_repo_one_parent) — DB 까지 가기 전에 422."""
        if (product_id is None) == (project_id is None):
            raise ValidationError(
                "product / project 둘 중 정확히 하나에 연결해야 합니다"
            )
        if product_id is not None:
            if await self._product_repo.get(session, product_id) is None:
                raise NotFoundError(f"product not found: {product_id}")
        if project_id is not None:
            if await self._project_repo.get(session, project_id) is None:
                raise NotFoundError(f"project not found: {project_id}")

    async def _check_token(self, session: AsyncSession, token_id: int | None) -> None:
        """git_token_id 가 오면 행이 있어야 한다. None 은 무토큰."""
        if token_id is None:
            return
        if await self._git_token_repo.get(session, token_id) is None:
            raise NotFoundError(f"git_token not found: {token_id}")

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> RepoDTO:
        fields["slug"] = self._check_slug(fields["slug"])
        await self._check_token(session, fields.get("git_token_id"))
        await self._check_parent(
            session, fields.get("product_id"), fields.get("project_id")
        )
        if await self._repo_repo.get_by_slug(session, fields["slug"]) is not None:
            raise ConflictError(f"이미 등록된 레포입니다: {fields['slug']}")
        return await self._repo_repo.create(session, fields)

    async def update(
        self, session: AsyncSession, repo_id: int, fields: dict[str, Any]
    ) -> RepoDTO:
        current = await self._repo_repo.get(session, repo_id)
        if current is None:
            raise NotFoundError(f"repo not found: {repo_id}")
        if "slug" in fields:
            if fields["slug"] is None:
                raise ValidationError("slug cannot be null")
            fields["slug"] = self._check_slug(fields["slug"])
            if fields["slug"] != current.slug:
                if await self._repo_repo.get_by_slug(session, fields["slug"]):
                    raise ConflictError(f"이미 등록된 레포입니다: {fields['slug']}")
        if "enabled" in fields and fields["enabled"] is None:
            raise ValidationError("enabled cannot be null")
        if "git_token_id" in fields:
            await self._check_token(session, fields["git_token_id"])
        # 부모 이동 — 한쪽만 바뀌어도 결과 상태로 「정확히 하나」를 다시 본다.
        if "product_id" in fields or "project_id" in fields:
            await self._check_parent(
                session,
                fields.get("product_id", current.product_id),
                fields.get("project_id", current.project_id),
            )
        dto = await self._repo_repo.update(session, repo_id, fields)
        assert dto is not None  # 방금 존재를 확인했다
        return dto

    async def delete(self, session: AsyncSession, repo_id: int) -> None:
        """가드 없음 — 커밋은 CASCADE. 잔디를 남기려면 삭제 대신 enabled=false."""
        if not await self._repo_repo.delete(session, repo_id):
            raise NotFoundError(f"repo not found: {repo_id}")


repo_service = RepoService(
    RepoRepository(), ProductRepository(), ProjectRepository(), GitTokenRepository()
)
