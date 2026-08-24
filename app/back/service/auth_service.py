"""인증 — 2층. 자격 검증과 토큰 발급. HTTP(쿠키·상태코드)를 모른다."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import UnauthorizedError
from core.security import create_access_token, verify_password
from dto.user import UserDTO
from repository.user_repo import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def login(
        self, session: AsyncSession, username: str, password: str
    ) -> tuple[UserDTO, str]:
        """자격 검증 후 (user, 세션 토큰). 아이디 존재 여부를 노출하지 않는다 —
        불일치는 전부 동일한 UnauthorizedError 다."""
        user = await self._user_repo.get_by_username(session, username)
        if user is None or not verify_password(password, user.password_hash):
            raise UnauthorizedError("invalid credentials")
        token = create_access_token(
            username=user.username, uid=user.id, role=user.system_role
        )
        return user, token


auth_service = AuthService(UserRepository())
