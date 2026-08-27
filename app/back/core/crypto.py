"""토큰 암복호 — Fernet 대칭키. 키는 .env 의 GIT_TOKEN_KEY.

해시가 아니라 암호화인 이유 — 수집기가 GitHub 호출에 원문을 써야 해서
복호가 가능해야 한다. 키가 없으면 저장도 복호도 막는다(설정 누락을 조용히
무토큰으로 넘기지 않는다).

키 생성: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
"""

from __future__ import annotations

from cryptography.fernet import Fernet, InvalidToken

from config import get_settings
from core.exceptions import ValidationError


def _fernet() -> Fernet:
    key = get_settings().git_token_key
    if not key:
        raise ValidationError("GIT_TOKEN_KEY 가 .env 에 없습니다 — 토큰 암복호 불가")
    return Fernet(key.encode())


def encrypt_token(raw: str) -> str:
    return _fernet().encrypt(raw.encode()).decode()


def decrypt_token(cipher: str) -> str:
    try:
        return _fernet().decrypt(cipher.encode()).decode()
    except InvalidToken as exc:  # 키가 바뀌었거나 값이 깨졌다
        raise ValidationError("토큰 복호 실패 — GIT_TOKEN_KEY 가 저장 당시와 다릅니다") from exc
