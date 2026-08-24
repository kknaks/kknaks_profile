"""역할(career) — 2층."""

from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import ConflictError, NotFoundError, ValidationError
from dto.career import CareerDTO
from repository.career_repo import CareerRepository
from repository.company_repo import CompanyRepository
from repository.profile_repo import ProfileRepository

# DB 에서 NOT NULL — null 로 지우려는 요청은 여기서 막는다.
_NOT_NULLABLE = frozenset({"title", "started_on", "company_id"})


def _check_dates(started_on: date, ended_on: date | None) -> None:
    if ended_on is not None and ended_on < started_on:
        raise ValidationError("endedOn cannot be before startedOn")


class CareerService:
    def __init__(
        self,
        career_repo: CareerRepository,
        company_repo: CompanyRepository,
        profile_repo: ProfileRepository,
    ) -> None:
        self._career_repo = career_repo
        self._company_repo = company_repo
        self._profile_repo = profile_repo

    async def _require_company(self, session: AsyncSession, company_id: int) -> None:
        if await self._company_repo.get_by_id(session, company_id) is None:
            raise NotFoundError(f"company not found: {company_id}")

    async def list_careers(self, session: AsyncSession) -> list[CareerDTO]:
        return await self._career_repo.list_with_company(session)

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> CareerDTO:
        _check_dates(fields["started_on"], fields.get("ended_on"))
        await self._require_company(session, fields["company_id"])
        # profile_id 는 클라이언트가 정하지 않는다 — 1인 사이트라 첫 행이 곧 프로필이다.
        profile = await self._profile_repo.get_first(session)
        if profile is None:
            raise NotFoundError("profile not found")
        return await self._career_repo.create(
            session, {**fields, "profile_id": profile.id}
        )

    async def update(
        self, session: AsyncSession, career_id: int, fields: dict[str, Any]
    ) -> CareerDTO:
        for name in _NOT_NULLABLE & fields.keys():
            if fields[name] is None:
                raise ValidationError(f"{name} cannot be null")
        if "company_id" in fields:
            await self._require_company(session, fields["company_id"])
        # 날짜 일관성 — 한쪽만 바뀌어도 합쳐서 본다. 기존 행이 없으면 404.
        if "started_on" in fields or "ended_on" in fields:
            current = await self._career_repo.get(session, career_id)
            if current is None:
                raise NotFoundError(f"career not found: {career_id}")
            _check_dates(
                fields.get("started_on", current.started_on),
                fields.get("ended_on", current.ended_on),
            )
        dto = await self._career_repo.update(session, career_id, fields)
        if dto is None:
            raise NotFoundError(f"career not found: {career_id}")
        return dto

    async def delete(self, session: AsyncSession, career_id: int) -> None:
        """제품이 붙어 있으면 지우지 않는다 — FK CASCADE 가 제품까지 쓸어간다.

        company_service 의 career 가드와 같은 패턴.
        """
        count = await self._career_repo.product_count(session, career_id)
        if count > 0:
            raise ConflictError(
                f"제품 {count}개가 이 역할에 있습니다 — 제품을 먼저 옮기거나 지우세요"
            )
        problem_count = await self._career_repo.problem_count(session, career_id)
        if problem_count > 0:
            raise ConflictError(
                f"문제 {problem_count}개가 이 역할에 있습니다 — 문제를 먼저 지우세요"
            )
        if not await self._career_repo.delete(session, career_id):
            raise NotFoundError(f"career not found: {career_id}")


career_service = CareerService(CareerRepository(), CompanyRepository(), ProfileRepository())
