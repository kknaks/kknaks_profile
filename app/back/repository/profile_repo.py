"""profile 표 접근 — 3층."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundError
from dto.profile import ProfileDTO
from models import Profile


def _to_dto(row: Profile) -> ProfileDTO:
    return ProfileDTO(
        id=row.id,
        handle=row.handle,
        name=row.name,
        role=row.role,
        years=row.years,
        location=row.location,
        focus=row.focus,
        avatar_url=row.avatar_url,
        email=row.email,
        github=row.github,
        linkedin=row.linkedin,
        stack=row.stack,
    )


class ProfileRepository:
    async def get_first(self, session: AsyncSession) -> ProfileDTO | None:
        """루트 프로필 — 사이트 주인은 한 명이라 첫 행이 곧 프로필이다."""
        row = (
            await session.execute(select(Profile).order_by(Profile.id).limit(1))
        ).scalar_one_or_none()
        return _to_dto(row) if row else None

    async def update_first(
        self, session: AsyncSession, fields: dict[str, Any]
    ) -> ProfileDTO:
        """첫 행에 `fields` 만 얹는다 — PATCH 시맨틱. flush 까지만 (commit 은 get_db)."""
        row = (
            await session.execute(select(Profile).order_by(Profile.id).limit(1))
        ).scalar_one_or_none()
        if row is None:
            raise NotFoundError("profile not found")
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        return _to_dto(row)
