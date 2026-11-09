"""접속 게이트 — 내부 공유용 비밀번호 하나(DEC-005 D2).

- POST /api/auth/session — 비밀번호 검증 → 세션 쿠키 발급
- GET  /api/auth/session — 세션 유효 확인

계정·권한 등급·rate limit 을 두지 않는다. 시도 횟수 제한도 없다(내부 공유 전제).
**비밀번호 값은 로그·응답 어디에도 나가지 않는다.**
"""

from __future__ import annotations

from fastapi import APIRouter, Cookie, HTTPException, Response
from pydantic import BaseModel, Field

from api.deps import issue_session, password_configured, verify_session
from config import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])


class SessionRequest(BaseModel):
    password: str = Field(min_length=1)


class SessionResponse(BaseModel):
    ok: bool


@router.post("/session", response_model=SessionResponse)
def create_session(body: SessionRequest, response: Response) -> SessionResponse:
    if not password_configured():
        # env 미주입이면 빈 비밀번호로 열리지 않게 명시적으로 거부한다.
        # 「기본값이 없다」가 「아무나 들어온다」가 되면 게이트가 아니다.
        raise HTTPException(status_code=503, detail="PASSWORD_NOT_CONFIGURED")
    if body.password != settings.demo_password:
        raise HTTPException(status_code=401, detail="INVALID_PASSWORD")

    response.set_cookie(
        key=settings.session_cookie_name,
        value=issue_session(),
        max_age=settings.session_max_age_sec,
        httponly=True,
        # 배포는 Vercel(프론트) ↔ 홈서버(API) 교차 사이트다 — `Lax` 면 쿠키가 실리지
        # 않아 게이트를 통과해도 다음 요청이 401 이다. `secure` 에서 파생한다(config.py).
        samesite=settings.session_cookie_samesite,
        secure=settings.session_cookie_secure,
        path="/",
    )
    return SessionResponse(ok=True)


@router.get("/session", response_model=SessionResponse)
def check_session(
    ontology_demo_sid: str | None = Cookie(default=None),
) -> SessionResponse:
    if not verify_session(ontology_demo_sid):
        raise HTTPException(status_code=401, detail="NO_SESSION")
    return SessionResponse(ok=True)


@router.delete("/session", response_model=SessionResponse)
def drop_session(response: Response) -> SessionResponse:
    # 발급과 **같은 속성**으로 지운다 — 속성이 다르면 브라우저가 다른 쿠키로 보고 남긴다.
    response.delete_cookie(
        settings.session_cookie_name, path="/",
        samesite=settings.session_cookie_samesite, secure=settings.session_cookie_secure)
    return SessionResponse(ok=True)
