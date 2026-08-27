"""라우터 공용 의존성 — 세션 · 인증 게이트."""

from __future__ import annotations

from fastapi import Request

from config import get_settings
from core.db import get_db  # noqa: F401 — 라우터가 여기서 가져다 쓴다
from core.exceptions import UnauthorizedError
from core.security import decode_access_token


def require_admin(request: Request) -> dict:
    """세션 쿠키 JWT 검증. 부재/만료/위조면 401. 성공하면 payload 반환.

    admin API 는 전부 `Depends(require_admin)` 로 이 게이트를 재사용한다.
    """
    token = request.cookies.get(get_settings().auth_cookie_name)
    payload = decode_access_token(token) if token else None
    if not payload:
        raise UnauthorizedError("not authenticated")
    return payload
