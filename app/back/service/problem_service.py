"""해결한 문제(problem) — 2층."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundError, ValidationError
from dto.problem import ProblemDTO
from repository.career_repo import CareerRepository
from repository.problem_repo import ProblemRepository
from repository.product_repo import ProductRepository

# DB 에서 NOT NULL — null 로 지우려는 요청은 여기서 막는다.
_NOT_NULLABLE = frozenset({"title", "career_id", "display_order"})


class ProblemService:
    def __init__(
        self,
        problem_repo: ProblemRepository,
        career_repo: CareerRepository,
        product_repo: ProductRepository,
    ) -> None:
        self._problem_repo = problem_repo
        self._career_repo = career_repo
        self._product_repo = product_repo

    async def _require_career(self, session: AsyncSession, career_id: int) -> None:
        if await self._career_repo.get(session, career_id) is None:
            raise NotFoundError(f"career not found: {career_id}")

    async def _require_product_of_career(
        self, session: AsyncSession, product_id: int, career_id: int
    ) -> None:
        """제품 존재 + 소속 검증 — 문제는 역할의 것이고 제품도 그 역할의 것이어야 한다."""
        product = await self._product_repo.get(session, product_id)
        if product is None:
            raise NotFoundError(f"product not found: {product_id}")
        if product.career_id != career_id:
            raise ValidationError("제품이 그 역할의 것이 아닙니다")

    async def list_problems(self, session: AsyncSession) -> list[ProblemDTO]:
        return await self._problem_repo.list_with_names(session)

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> ProblemDTO:
        await self._require_career(session, fields["career_id"])
        if fields.get("product_id") is not None:
            await self._require_product_of_career(
                session, fields["product_id"], fields["career_id"]
            )
        return await self._problem_repo.create(session, fields)

    async def update(
        self, session: AsyncSession, problem_id: int, fields: dict[str, Any]
    ) -> ProblemDTO:
        for name in _NOT_NULLABLE & fields.keys():
            if fields[name] is None:
                raise ValidationError(f"{name} cannot be null")
        if "career_id" in fields:
            await self._require_career(session, fields["career_id"])
        # 소속 일관성 — 한쪽만 바뀌어도 합쳐서 본다. 기존 행이 없으면 404.
        if "career_id" in fields or fields.get("product_id") is not None:
            current = await self._problem_repo.get(session, problem_id)
            if current is None:
                raise NotFoundError(f"problem not found: {problem_id}")
            career_id = fields.get("career_id", current.career_id)
            product_id = (
                fields["product_id"] if "product_id" in fields else current.product_id
            )
            if product_id is not None:
                await self._require_product_of_career(session, product_id, career_id)
        dto = await self._problem_repo.update(session, problem_id, fields)
        if dto is None:
            raise NotFoundError(f"problem not found: {problem_id}")
        return dto

    async def delete(self, session: AsyncSession, problem_id: int) -> None:
        if not await self._problem_repo.delete(session, problem_id):
            raise NotFoundError(f"problem not found: {problem_id}")


problem_service = ProblemService(
    ProblemRepository(), CareerRepository(), ProductRepository()
)
