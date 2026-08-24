"""product 표 접근 — 3층."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.product import ProductDTO
from models import Career, Company, Product


def _to_dto(row: Product, career_title: str, company_name: str) -> ProductDTO:
    return ProductDTO(
        id=row.id,
        career_id=row.career_id,
        career_title=career_title,
        company_name=company_name,
        slug=row.slug,
        title=row.title,
        summary=row.summary,
        detail_path=row.detail_path,
        category=row.category,
        status=row.status,
        started_on=row.started_on,
        stack=row.stack,
        thumbnail=row.thumbnail,
        links=row.links,
        visible=row.visible,
    )


# product → career → company 2단 조인 — 회사는 career 를 거쳐 닿는다(erd.md §product).
_JOINED = (
    select(Product, Career.title, Company.name)
    .join(Career, Career.id == Product.career_id)
    .join(Company, Company.id == Career.company_id)
)


class ProductRepository:
    async def list_with_career(self, session: AsyncSession) -> list[ProductDTO]:
        """제품 + 역할·회사 이름. started_on DESC NULLS LAST."""
        stmt = _JOINED.order_by(
            Product.started_on.desc().nulls_last(), Product.id.desc()
        )
        rows = (await session.execute(stmt)).all()
        return [_to_dto(product, career_title, company_name) for product, career_title, company_name in rows]

    async def get(self, session: AsyncSession, product_id: int) -> ProductDTO | None:
        row = (
            await session.execute(_JOINED.where(Product.id == product_id))
        ).one_or_none()
        return _to_dto(row[0], row[1], row[2]) if row else None

    async def get_by_slug(self, session: AsyncSession, slug: str) -> ProductDTO | None:
        row = (
            await session.execute(_JOINED.where(Product.slug == slug))
        ).one_or_none()
        return _to_dto(row[0], row[1], row[2]) if row else None

    async def _career_names(self, session: AsyncSession, career_id: int) -> tuple[str, str]:
        return (
            await session.execute(
                select(Career.title, Company.name)
                .join(Company, Company.id == Career.company_id)
                .where(Career.id == career_id)
            )
        ).one()

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> ProductDTO:
        row = Product(**fields)
        session.add(row)
        await session.flush()
        return _to_dto(row, *await self._career_names(session, row.career_id))

    async def update(
        self, session: AsyncSession, product_id: int, fields: dict[str, Any]
    ) -> ProductDTO | None:
        """보낸 필드만 얹는다 — PATCH 시맨틱. 없는 id 면 None, 판단은 service."""
        row = await session.get(Product, product_id)
        if row is None:
            return None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        return _to_dto(row, *await self._career_names(session, row.career_id))

    async def delete(self, session: AsyncSession, product_id: int) -> bool:
        row = await session.get(Product, product_id)
        if row is None:
            return False
        await session.delete(row)
        await session.flush()
        return True
