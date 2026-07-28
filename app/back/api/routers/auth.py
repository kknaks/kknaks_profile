"""관리자 인증 — 로그인/세션/로그아웃 (KDEV-SPEC-006 / WORK-011).

- POST /api/auth/login  — 자격 검증 후 httpOnly 쿠키 JWT 발급
- POST /api/auth/logout — 세션 쿠키 만료
- GET  /api/auth/me     — 현재 세션 계정 반환 (require_admin)

세션은 httpOnly 쿠키에 담긴 HS256 JWT. FE 스크립트는 토큰을 만지지 않는다(SPEC-006 §Data Contract).
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import config
from core.db import get_db
from core.models import User
from core.security import create_access_token, decode_access_token, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class UserOut(BaseModel):
    username: str
    role: str


def _set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=config.auth_cookie_name(),
        value=token,
        max_age=config.jwt_expire_minutes() * 60,
        httponly=True,
        samesite="lax",
        secure=config.auth_cookie_secure(),
        domain=config.auth_cookie_domain(),
        path="/",
    )


def require_admin(request: Request) -> dict:
    """세션 쿠키 JWT 를 검증. 부재/만료/위조면 401. 성공하면 payload 반환.

    후속 admin API 는 `Depends(require_admin)` 로 이 게이트를 재사용한다.
    """
    token = request.cookies.get(config.auth_cookie_name())
    payload = decode_access_token(token) if token else None
    if not payload:
        raise HTTPException(status_code=401, detail="not authenticated")
    return payload


@router.post("/login")
async def login(body: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user = (
        await db.execute(select(User).where(User.username == body.username))
    ).scalar_one_or_none()
    # 아이디 존재 여부를 노출하지 않는다 — 불일치는 전부 동일한 401 (SPEC-006 §5).
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")

    token = create_access_token(username=user.username, uid=user.id, role=user.role)
    _set_session_cookie(response, token)
    return {"user": UserOut(username=user.username, role=user.role)}


@router.post("/logout")
def logout(response: Response):
    """멱등 — 세션 유무와 무관하게 쿠키를 만료시킨다."""
    response.delete_cookie(
        key=config.auth_cookie_name(),
        domain=config.auth_cookie_domain(),
        path="/",
    )
    return {"ok": True}


@router.get("/me")
def me(payload: dict = Depends(require_admin)):
    return {"user": UserOut(username=payload["sub"], role=payload.get("role", "admin"))}
