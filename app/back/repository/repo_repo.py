"""repo 표 접근 — 3층."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.repo import RepoDTO
from models import Product, Project, Repo


def _to_dto(row: Repo, product_title: str | None, project_title: str | None) -> RepoDTO:
    return RepoDTO(
        id=row.id,
        product_id=row.product_id,
        project_id=row.project_id,
        product_title=product_title,
        project_title=project_title,
        slug=row.slug,
        role=row.role,
        git_token_id=row.git_token_id,
        enabled=row.enabled,
        last_fetched_at=row.last_fetched_at,
        last_error=row.last_error,
    )


# 부모가 둘 중 하나라 둘 다 outer join — 없는 쪽은 NULL 로 온다.
_JOINED = (
    select(Repo, Product.title, Project.title)
    .outerjoin(Product, Product.id == Repo.product_id)
    .outerjoin(Project, Project.id == Repo.project_id)
)


class RepoRepository:
    async def list_with_parent(self, session: AsyncSession) -> list[RepoDTO]:
        """레포 + 부모 이름. slug 순 — 목록이 짧아 가나다·알파벳이면 충분하다."""
        stmt = _JOINED.order_by(Repo.slug)
        rows = (await session.execute(stmt)).all()
        return [_to_dto(repo, p_title, j_title) for repo, p_title, j_title in rows]

    async def list_enabled(self, session: AsyncSession) -> list[RepoDTO]:
        """수집 대상 — enabled=true 만. 수집기가 읽는다."""
        stmt = _JOINED.where(Repo.enabled.is_(True)).order_by(Repo.slug)
        rows = (await session.execute(stmt)).all()
        return [_to_dto(repo, p_title, j_title) for repo, p_title, j_title in rows]

    async def get(self, session: AsyncSession, repo_id: int) -> RepoDTO | None:
        row = (
            await session.execute(_JOINED.where(Repo.id == repo_id))
        ).one_or_none()
        return _to_dto(row[0], row[1], row[2]) if row else None

    async def get_by_slug(self, session: AsyncSession, slug: str) -> RepoDTO | None:
        row = (
            await session.execute(_JOINED.where(Repo.slug == slug))
        ).one_or_none()
        return _to_dto(row[0], row[1], row[2]) if row else None

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> RepoDTO:
        row = Repo(**fields)
        session.add(row)
        await session.flush()
        dto = await self.get(session, row.id)
        assert dto is not None  # 방금 넣었다
        return dto

    async def update(
        self, session: AsyncSession, repo_id: int, fields: dict[str, Any]
    ) -> RepoDTO | None:
        """보낸 필드만 얹는다 — PATCH 시맨틱. 없는 id 면 None, 판단은 service."""
        row = await session.get(Repo, repo_id)
        if row is None:
            return None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        return await self.get(session, repo_id)

    async def delete(self, session: AsyncSession, repo_id: int) -> bool:
        row = await session.get(Repo, repo_id)
        if row is None:
            return False
        await session.delete(row)
        await session.flush()
        return True
