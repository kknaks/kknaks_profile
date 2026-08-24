"""career 표 접근 — 3층."""

from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.career import CareerDTO
from models import Career, Company, Problem, Product


def _to_dto(row: Career, company_name: str) -> CareerDTO:
    return CareerDTO(
        id=row.id,
        profile_id=row.profile_id,
        company_id=row.company_id,
        company_name=company_name,
        title=row.title,
        started_on=row.started_on,
        ended_on=row.ended_on,
        summary=row.summary,
        description=row.description,
        stack=row.stack,
    )


class CareerRepository:
    async def list_with_company(self, session: AsyncSession) -> list[CareerDTO]:
        """역할 + 회사 이름. started_on DESC — 파생 정렬(erd: display_order 는 컬럼이 아니다)."""
        stmt = (
            select(Career, Company.name)
            .join(Company, Company.id == Career.company_id)
            .order_by(Career.started_on.desc(), Career.id.desc())
        )
        rows = (await session.execute(stmt)).all()
        return [_to_dto(career, name) for career, name in rows]

    async def get(self, session: AsyncSession, career_id: int) -> CareerDTO | None:
        stmt = (
            select(Career, Company.name)
            .join(Company, Company.id == Career.company_id)
            .where(Career.id == career_id)
        )
        row = (await session.execute(stmt)).one_or_none()
        return _to_dto(row[0], row[1]) if row else None

    async def _company_name(self, session: AsyncSession, company_id: int) -> str:
        return (
            await session.execute(select(Company.name).where(Company.id == company_id))
        ).scalar_one()

    async def product_count(self, session: AsyncSession, career_id: int) -> int:
        """이 역할에 붙은 제품 수 — 삭제 가드용(company_repo.career_count 와 같은 자리)."""
        return (
            await session.execute(
                select(func.count(Product.id)).where(Product.career_id == career_id)
            )
        ).scalar_one()

    async def problem_count(self, session: AsyncSession, career_id: int) -> int:
        """이 역할에 붙은 문제 수 — 삭제 가드용(product_count 와 같은 자리)."""
        return (
            await session.execute(
                select(func.count(Problem.id)).where(Problem.career_id == career_id)
            )
        ).scalar_one()

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> CareerDTO:
        row = Career(**fields)
        session.add(row)
        await session.flush()
        return _to_dto(row, await self._company_name(session, row.company_id))

    async def update(
        self, session: AsyncSession, career_id: int, fields: dict[str, Any]
    ) -> CareerDTO | None:
        """보낸 필드만 얹는다 — PATCH 시맨틱. 없는 id 면 None, 판단은 service."""
        row = await session.get(Career, career_id)
        if row is None:
            return None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        return _to_dto(row, await self._company_name(session, row.company_id))

    async def delete(self, session: AsyncSession, career_id: int) -> bool:
        row = await session.get(Career, career_id)
        if row is None:
            return False
        await session.delete(row)
        await session.flush()
        return True
