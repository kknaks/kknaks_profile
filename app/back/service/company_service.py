"""회사 — 2층."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import ConflictError, NotFoundError, ValidationError
from dto.company import CompanyDTO, CompanyStatsDTO
from repository.company_repo import CompanyRepository

# DB 에서 NOT NULL — null 로 지우려는 요청은 여기서 막는다.
_NOT_NULLABLE = frozenset({"slug", "name"})


class CompanyService:
    def __init__(self, company_repo: CompanyRepository) -> None:
        self._company_repo = company_repo

    async def list_companies(self, session: AsyncSession) -> list[CompanyStatsDTO]:
        return await self._company_repo.list_with_stats(session)

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> CompanyDTO:
        if await self._company_repo.get_by_slug(session, fields["slug"]):
            raise ConflictError(f"slug already exists: {fields['slug']}")
        return await self._company_repo.create(session, fields)

    async def update(
        self, session: AsyncSession, company_id: int, fields: dict[str, Any]
    ) -> CompanyDTO:
        for name in _NOT_NULLABLE & fields.keys():
            if fields[name] is None:
                raise ValidationError(f"{name} cannot be null")
        if "slug" in fields:
            existing = await self._company_repo.get_by_slug(session, fields["slug"])
            if existing and existing.id != company_id:
                raise ConflictError(f"slug already exists: {fields['slug']}")
        dto = await self._company_repo.update(session, company_id, fields)
        if dto is None:
            raise NotFoundError(f"company not found: {company_id}")
        return dto

    async def delete(self, session: AsyncSession, company_id: int) -> None:
        """역할이 붙어 있으면 지우지 않는다 — FK CASCADE 가 역할·문제까지 쓸어간다."""
        count = await self._company_repo.career_count(session, company_id)
        if count > 0:
            raise ConflictError(f"역할 {count}개가 이 회사에 있습니다 — 역할을 먼저 지우세요")
        if not await self._company_repo.delete(session, company_id):
            raise NotFoundError(f"company not found: {company_id}")


company_service = CompanyService(CompanyRepository())
