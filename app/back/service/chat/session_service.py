"""익명 세션 — 쿠키의 반대편 (DEC-026 · SPEC-017 §4 세션 쿠키).

상태는 서버가 갖고 클라이언트는 열쇠(쿠키)만 갖는다. 이 층은 **HTTP 를 모른다** —
쿠키를 굽고 심는 것은 라우터이고, 여기는 「불투명 토큰 문자열 ↔ 세션 id」만 안다.

## 원문을 저장하지 않는다

DB 에는 sha256 해시만 둔다. 검증은 해시 비교라 원문이 필요 없고, DB 가 새도 남의
쿠키를 복원해 대화를 열 수 없다. 쿠키는 사용자 비밀번호가 아니라 **열쇠**라 해시에
salt·KDF 를 쓰지 않는다 — 값이 이미 128비트 난수라 사전 공격 대상이 아니다.

## 발급 시점이 계약이다

「채팅 첫 사용이 발급 시점」(DEC-026 D1). 그래서 `resolve` 는 세션을 **만들지 않고**,
만드는 것은 `resolve_or_create` 뿐이다 — 그것을 부르는 곳은 대화 생성 하나다.
목록 조회가 세션을 만들면 사이트를 열어만 본 방문자에게 row 가 생긴다.
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from repository.chat_repo import ChatRepository, chat_repository


def hash_token(raw: str) -> str:
    """쿠키 값 → 저장·조회 키. 이 함수 하나가 해시 규약의 정본이다."""
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def new_token() -> str:
    """서버 발급 불투명 토큰. UUID 대신 `token_urlsafe` — 같은 128비트인데 더 짧다."""
    return secrets.token_urlsafe(32)


class ChatSessionService:
    def __init__(self, repo: ChatRepository) -> None:
        self._repo = repo

    async def resolve(
        self, session: AsyncSession, raw_token: str | None
    ) -> int | None:
        """쿠키로 세션 id 를 찾는다. **없으면 만들지 않고 None** (DEC-026 D1).

        찾았으면 `last_seen_at` 을 민다 — sliding 의 **서버 쪽** 절반이다. 나머지
        절반(브라우저 쪽 만료 연장)은 라우터가 매 응답에 쿠키를 다시 구워서 한다.
        둘 다 있어야 「사용할 때마다 연장」(§4 · S-5 3항)이 실제로 성립한다 — 서버만
        밀면 브라우저 쿠키가 최초 발급 +30일에 죽고, 쿠키만 다시 구우면 서버 row 가
        영원히 산다.
        """
        if not raw_token:
            return None
        now = datetime.now(UTC)
        session_id = await self._repo.get_session_id(
            session,
            hash_token(raw_token),
            # 마지막 사용에서 30일이 지났으면 없는 것으로 본다 — 쿠키 Max-Age 와
            # 같은 값을 쓴다. 두 만료가 갈리면 한쪽만 살아 있는 구간이 생긴다.
            not_before=now - timedelta(seconds=get_settings().chat_cookie_max_age_sec),
        )
        if session_id is None:
            # 쿠키는 있는데 살아 있는 row 가 없다(만료·DB 교체). 새 손님과 같다 —
            # 여기서 만들지 않는다. 대화 생성이 오면 그때 새 세션이 발급된다.
            return None
        await self._repo.touch_session(session, session_id, now=now)
        return session_id

    async def resolve_or_create(
        self, session: AsyncSession, raw_token: str | None
    ) -> tuple[int, str]:
        """세션 id 를 보장한다. 반환 = `(session_id, 쿠키에 심을 값)`.

        두 번째 값은 **항상** 심어야 하는 값이다 — 새로 발급했든 쓰던 것이든. 「새로
        만들었을 때만 심는다」로 두면 재방문자의 쿠키 만료가 최초 발급 시점에 고정돼
        sliding 이 브라우저 쪽에서 성립하지 않는다(W1).

        쿠키 굽는 규약(httpOnly · Lax · Secure · Max-Age)은 라우터가 소유한다 —
        이 층은 HTTP 를 모른다.
        """
        existing = await self.resolve(session, raw_token)
        if existing is not None:
            return existing, raw_token or ""
        token = new_token()
        session_id = await self._repo.create_session(session, hash_token(token))
        return session_id, token


chat_session_service = ChatSessionService(chat_repository)
