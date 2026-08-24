"""users 표 접근 — 3층. AsyncSession 만 알고 HTTP 를 모른다."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.user import UserDTO
from models import User


class UserRepository:
    async def get_by_username(
        self, session: AsyncSession, username: str
    ) -> UserDTO | None:
        row = (
            await session.execute(select(User).where(User.username == username))
        ).scalar_one_or_none()
        if row is None:
            return None
        return UserDTO(
            id=row.id,
            profile_id=row.profile_id,
            username=row.username,
            password_hash=row.password_hash,
            system_role=row.system_role,
        )
