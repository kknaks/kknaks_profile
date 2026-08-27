"""제품(product) — 2층."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import ConflictError, NotFoundError, ValidationError
from dto.product import ProductDTO
from repository.career_repo import CareerRepository
from repository.product_repo import ProductRepository

# DB 에서 NOT NULL — null 로 지우려는 요청은 여기서 막는다.
_NOT_NULLABLE = frozenset({"slug", "title", "career_id", "visible"})


class ProductService:
    def __init__(
        self, product_repo: ProductRepository, career_repo: CareerRepository
    ) -> None:
        self._product_repo = product_repo
        self._career_repo = career_repo

    async def _require_career(self, session: AsyncSession, career_id: int) -> None:
        if await self._career_repo.get(session, career_id) is None:
            raise NotFoundError(f"career not found: {career_id}")

    async def _require_free_slug(
        self, session: AsyncSession, slug: str, exclude_id: int | None = None
    ) -> None:
        existing = await self._product_repo.get_by_slug(session, slug)
        if existing and existing.id != exclude_id:
            raise ConflictError(f"slug already exists: {slug}")

    async def list_products(self, session: AsyncSession) -> list[ProductDTO]:
        return await self._product_repo.list_with_career(session)

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> ProductDTO:
        await self._require_career(session, fields["career_id"])
        await self._require_free_slug(session, fields["slug"])
        return await self._product_repo.create(session, fields)

    async def update(
        self, session: AsyncSession, product_id: int, fields: dict[str, Any]
    ) -> ProductDTO:
        for name in _NOT_NULLABLE & fields.keys():
            if fields[name] is None:
                raise ValidationError(f"{name} cannot be null")
        if "career_id" in fields:
            await self._require_career(session, fields["career_id"])
        if "slug" in fields:
            await self._require_free_slug(session, fields["slug"], exclude_id=product_id)
        dto = await self._product_repo.update(session, product_id, fields)
        if dto is None:
            raise NotFoundError(f"product not found: {product_id}")
        return dto

    async def delete(self, session: AsyncSession, product_id: int) -> None:
        if not await self._product_repo.delete(session, product_id):
            raise NotFoundError(f"product not found: {product_id}")


product_service = ProductService(ProductRepository(), CareerRepository())
