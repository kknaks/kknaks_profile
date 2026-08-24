"""관리자 인증 — 1층. 쿠키와 상태코드는 여기까지만 안다.

- POST /api/auth/login  — 자격 검증 후 httpOnly 쿠키 JWT 발급
- POST /api/auth/logout — 세션 쿠키 만료 (멱등)
- GET  /api/auth/me     — 현재 세션 계정 반환
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from config import get_settings
from schemas.auth import LoginRequest, LoginResponse, LogoutResponse, UserOut
from service.auth_service import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _set_session_cookie(response: Response, token: str) -> None:
    settings = get_settings()
    response.set_cookie(
        key=settings.auth_cookie_name,
        value=token,
        max_age=settings.jwt_expire_minutes * 60,
        httponly=True,
        samesite="lax",
        secure=settings.auth_cookie_secure,
        domain=settings.auth_cookie_domain,
        path="/",
    )


@router.post("/login", response_model=LoginResponse)
async def login(
    body: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)
) -> LoginResponse:
    user, token = await auth_service.login(db, body.username, body.password)
    _set_session_cookie(response, token)
    return LoginResponse(user=UserOut(username=user.username, role=user.system_role))


@router.post("/logout", response_model=LogoutResponse)
def logout(response: Response) -> LogoutResponse:
    settings = get_settings()
    response.delete_cookie(
        key=settings.auth_cookie_name,
        domain=settings.auth_cookie_domain,
        path="/",
    )
    return LogoutResponse(ok=True)


@router.get("/me", response_model=LoginResponse)
def me(payload: dict = Depends(require_admin)) -> LoginResponse:
    return LoginResponse(
        user=UserOut(username=payload["sub"], role=payload.get("role", "admin"))
    )
