"""company 표 접근 — 3층."""

from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.company import CompanyDTO, CompanyStatsDTO
from models import Career, Company


def _to_dto(row: Company) -> CompanyDTO:
    return CompanyDTO(
        id=row.id,
        slug=row.slug,
        name=row.name,
        description=row.description,
        location=row.location,
        site=row.site,
        logo_url=row.logo_url,
        github_org=row.github_org,
    )


class CompanyRepository:
    async def list_with_stats(self, session: AsyncSession) -> list[CompanyStatsDTO]:
        """회사 + career 파생값. 최신 역할 시작일 내림차순, 역할 없는 회사는 뒤로."""
        stmt = (
            select(
                Company,
                func.count(Career.id),
                func.min(Career.started_on),
                func.max(Career.ended_on),
                func.bool_or(Career.ended_on.is_(None)),
            )
            .outerjoin(Career, Career.company_id == Company.id)
            .group_by(Company.id)
            .order_by(func.max(Career.started_on).desc().nulls_last(), Company.id)
        )
        rows = (await session.execute(stmt)).all()
        return [
            CompanyStatsDTO(
                company=_to_dto(company),
                career_count=count,
                started_on=started,
                ended_on=ended,
                is_current=bool(current),
            )
            for company, count, started, ended, current in rows
        ]

    async def get_by_id(self, session: AsyncSession, company_id: int) -> CompanyDTO | None:
        row = await session.get(Company, company_id)
        return _to_dto(row) if row else None

    async def get_by_slug(self, session: AsyncSession, slug: str) -> CompanyDTO | None:
        row = (
            await session.execute(select(Company).where(Company.slug == slug))
        ).scalar_one_or_none()
        return _to_dto(row) if row else None

    async def career_count(self, session: AsyncSession, company_id: int) -> int:
        return (
            await session.execute(
                select(func.count(Career.id)).where(Career.company_id == company_id)
            )
        ).scalar_one()

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> CompanyDTO:
        row = Company(**fields)
        session.add(row)
        await session.flush()
        return _to_dto(row)

    async def update(
        self, session: AsyncSession, company_id: int, fields: dict[str, Any]
    ) -> CompanyDTO | None:
        """보낸 필드만 얹는다 — PATCH 시맨틱. 없는 id 면 None, 판단은 service."""
        row = await session.get(Company, company_id)
        if row is None:
            return None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        return _to_dto(row)

    async def delete(self, session: AsyncSession, company_id: int) -> bool:
        row = await session.get(Company, company_id)
        if row is None:
            return False
        await session.delete(row)
        await session.flush()
        return True
