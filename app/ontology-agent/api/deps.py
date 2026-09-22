"""API 공통 의존 — 세션 검증 · DB · 에러 변환.

세션 저장 방식(WORK-002 Open Issue): **서명 쿠키**를 쓴다. 서버 보관(테이블·메모리)을
고르지 않은 이유는 셋이다 —
1. work-002 「Domain / Schema」가 **테이블을 새로 만들지 않는 범위**를 요구한다.
2. 메모리 보관은 프로세스가 죽으면 전원 재입력이고, 우리 배포는 컨테이너 재기동이 잦다.
3. 세션에 담을 것이 「비밀번호를 통과했다」 한 비트뿐이라 조회할 상태가 없다.

서명은 비밀번호에서 파생한 키로 HMAC 한다 — 비밀번호가 바뀌면 기존 세션이 자동 무효다.
"""

from __future__ import annotations

import hashlib
import hmac
import time

from fastapi import Cookie, HTTPException

from config import settings
from service.errors import QueryError

_SEPARATOR = "."


def _signing_key() -> bytes:
    """비밀번호에서 파생한 서명 키. **원문을 쿠키에 넣지 않는다.**"""
    return hashlib.sha256(
        b"ontology-demo-session|" + settings.demo_password.encode("utf-8")
    ).digest()


def issue_session() -> str:
    """`<만료 epoch>.<HMAC>` — 서버가 상태를 들고 있지 않아도 검증된다."""
    expires = int(time.time()) + settings.session_max_age_sec
    payload = str(expires)
    sig = hmac.new(_signing_key(), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{payload}{_SEPARATOR}{sig}"


def password_configured() -> bool:
    return bool(settings.demo_password)


def verify_session(token: str | None) -> bool:
    # 비밀번호가 미주입이면 서명 키가 `sha256(b"ontology-demo-session|")` 라는 **레포에 적힌
    # 상수**가 된다 — 누구나 오프라인에서 유효한 토큰을 만들어 전 조회 API 를 연다.
    # 발급 경로(auth_router)는 이미 막았지만 검증 경로가 뚫려 있으면 발급이 필요 없다.
    # env 미주입은 데모 배포에서 가장 흔한 사고라 여기서 함께 닫는다.
    if not password_configured():
        return False
    if not token or _SEPARATOR not in token:
        return False
    payload, _, sig = token.rpartition(_SEPARATOR)
    expected = hmac.new(_signing_key(), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected):
        return False
    try:
        return int(payload) > int(time.time())
    except ValueError:
        return False


def require_session(
    ontology_demo_sid: str | None = Cookie(default=None),
) -> None:
    """세션 없으면 전 API 401 `NO_SESSION`(SPEC-003 S-5)."""
    if not verify_session(ontology_demo_sid):
        raise HTTPException(status_code=401, detail="NO_SESSION")


def as_http(exc: QueryError) -> HTTPException:
    """조회 거부 → HTTP. 본문은 `{"detail": "<코드>"}` 로 통일한다(SPEC-003 Case Matrix)."""
    return HTTPException(status_code=exc.http_status, detail=exc.code)
