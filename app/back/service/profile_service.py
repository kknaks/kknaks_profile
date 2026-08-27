"""프로필 — 2층."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundError, ValidationError
from dto.profile import ProfileDTO
from repository.profile_repo import ProfileRepository

# DB 에서 NOT NULL 인 컬럼 — null 로 지우려는 요청은 여기서 막는다.
_NOT_NULLABLE = frozenset({"handle", "name", "role", "email"})


class ProfileService:
    def __init__(self, profile_repo: ProfileRepository) -> None:
        self._profile_repo = profile_repo

    async def get_profile(self, session: AsyncSession) -> ProfileDTO:
        profile = await self._profile_repo.get_first(session)
        if profile is None:
            raise NotFoundError("profile not found")
        return profile

    async def update_profile(
        self, session: AsyncSession, fields: dict[str, Any]
    ) -> ProfileDTO:
        """보낸 필드만 반영한다 — fields 는 라우터가 exclude_unset 으로 거른 것."""
        for name in _NOT_NULLABLE & fields.keys():
            if fields[name] is None:
                raise ValidationError(f"{name} cannot be null")
        return await self._profile_repo.update_first(session, fields)


profile_service = ProfileService(ProfileRepository())
