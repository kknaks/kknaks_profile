"""problem 표 접근 — 3층."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.problem import ProblemDTO
from models import Career, Company, Problem, Product


def _to_dto(
    row: Problem, career_title: str, company_name: str, product_title: str | None
) -> ProblemDTO:
    return ProblemDTO(
        id=row.id,
        career_id=row.career_id,
        career_title=career_title,
        company_name=company_name,
        product_id=row.product_id,
        product_title=product_title,
        title=row.title,
        body=row.body,
        display_order=row.display_order,
        chat_exposed=row.chat_exposed,
    )


# problem → career → company 2단 조인 + product 는 NULL 허용이라 outer join.
_JOINED = (
    select(Problem, Career.title, Company.name, Product.title)
    .join(Career, Career.id == Problem.career_id)
    .join(Company, Company.id == Career.company_id)
    .join(Product, Product.id == Problem.product_id, isouter=True)
)


class ProblemRepository:
    async def list_with_names(self, session: AsyncSession) -> list[ProblemDTO]:
        """문제 + 역할·회사·제품 이름. 최근 역할 먼저, 그 안에서 display_order ASC."""
        stmt = _JOINED.order_by(
            Career.started_on.desc(), Problem.display_order.asc(), Problem.id.asc()
        )
        rows = (await session.execute(stmt)).all()
        return [_to_dto(*row) for row in rows]

    async def get(self, session: AsyncSession, problem_id: int) -> ProblemDTO | None:
        row = (
            await session.execute(_JOINED.where(Problem.id == problem_id))
        ).one_or_none()
        return _to_dto(*row) if row else None

    async def _names(
        self, session: AsyncSession, career_id: int, product_id: int | None
    ) -> tuple[str, str, str | None]:
        career_title, company_name = (
            await session.execute(
                select(Career.title, Company.name)
                .join(Company, Company.id == Career.company_id)
                .where(Career.id == career_id)
            )
        ).one()
        product_title = None
        if product_id is not None:
            product_title = (
                await session.execute(
                    select(Product.title).where(Product.id == product_id)
                )
            ).scalar_one_or_none()
        return career_title, company_name, product_title

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> ProblemDTO:
        row = Problem(**fields)
        session.add(row)
        await session.flush()
        return _to_dto(row, *await self._names(session, row.career_id, row.product_id))

    async def update(
        self, session: AsyncSession, problem_id: int, fields: dict[str, Any]
    ) -> ProblemDTO | None:
        """보낸 필드만 얹는다 — PATCH 시맨틱. 없는 id 면 None, 판단은 service."""
        row = await session.get(Problem, problem_id)
        if row is None:
            return None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        return _to_dto(row, *await self._names(session, row.career_id, row.product_id))

    async def delete(self, session: AsyncSession, problem_id: int) -> bool:
        row = await session.get(Problem, problem_id)
        if row is None:
            return False
        await session.delete(row)
        await session.flush()
        return True
