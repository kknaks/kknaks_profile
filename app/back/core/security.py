"""비밀번호 해시(bcrypt) · 쿠키 JWT(HS256).

- bcrypt 는 salt 내장 — users.password_hash 컬럼에 그대로 저장한다.
- JWT payload: {sub: username, uid, role, iat, exp}. 시크릿은 Settings.jwt_secret.
- 계약은 레거시와 동일 — 프론트 쿠키(kknaks_session)를 그대로 쓴다.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from config import get_settings


def hash_password(plain: str) -> str:
    """평문 → bcrypt 해시 문자열."""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """timing-safe 비교는 bcrypt.checkpw 내부에서 처리."""
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def create_access_token(*, username: str, uid: int, role: str) -> str:
    """로그인 성공 시 발급하는 세션 JWT."""
    settings = get_settings()
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "uid": uid,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.jwt_expire_minutes)).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def decode_access_token(token: str) -> dict | None:
    """유효하면 payload dict, 만료/위조면 None."""
    try:
        return jwt.decode(token, get_settings().jwt_secret, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None
