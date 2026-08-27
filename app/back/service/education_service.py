"""교육(education) — 2층."""

from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundError, ValidationError
from dto.education import EducationDTO
from repository.education_repo import EducationRepository
from repository.profile_repo import ProfileRepository

# DB 에서 NOT NULL — null 로 지우려는 요청은 여기서 막는다.
_NOT_NULLABLE = frozenset({"org", "title", "started_on"})


def _check_dates(started_on: date, ended_on: date | None) -> None:
    if ended_on is not None and ended_on < started_on:
        raise ValidationError("endedOn cannot be before startedOn")


class EducationService:
    def __init__(
        self,
        education_repo: EducationRepository,
        profile_repo: ProfileRepository,
    ) -> None:
        self._education_repo = education_repo
        self._profile_repo = profile_repo

    async def list_educations(self, session: AsyncSession) -> list[EducationDTO]:
        return await self._education_repo.list_all(session)

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> EducationDTO:
        _check_dates(fields["started_on"], fields.get("ended_on"))
        # profile_id 는 클라이언트가 정하지 않는다 — 1인 사이트라 첫 행이 곧 프로필이다.
        profile = await self._profile_repo.get_first(session)
        if profile is None:
            raise NotFoundError("profile not found")
        return await self._education_repo.create(
            session, {**fields, "profile_id": profile.id}
        )

    async def update(
        self, session: AsyncSession, education_id: int, fields: dict[str, Any]
    ) -> EducationDTO:
        for name in _NOT_NULLABLE & fields.keys():
            if fields[name] is None:
                raise ValidationError(f"{name} cannot be null")
        # 날짜 일관성 — 한쪽만 바뀌어도 합쳐서 본다. 기존 행이 없으면 404.
        if "started_on" in fields or "ended_on" in fields:
            current = await self._education_repo.get(session, education_id)
            if current is None:
                raise NotFoundError(f"education not found: {education_id}")
            _check_dates(
                fields.get("started_on", current.started_on),
                fields.get("ended_on", current.ended_on),
            )
        dto = await self._education_repo.update(session, education_id, fields)
        if dto is None:
            raise NotFoundError(f"education not found: {education_id}")
        return dto

    async def delete(self, session: AsyncSession, education_id: int) -> None:
        """가드 없음 — education 에는 아무것도 붙지 않는다(모델 주석: 커밋 미귀속)."""
        if not await self._education_repo.delete(session, education_id):
            raise NotFoundError(f"education not found: {education_id}")


education_service = EducationService(EducationRepository(), ProfileRepository())
