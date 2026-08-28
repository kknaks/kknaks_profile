"""turn 전용 Bearer 토큰 — 발급 · 검증 · 폐기 (DEC-027 D5).

## JWT 기계가 필요 없다

레퍼런스(mediness)는 사용자 JWT family 를 새로 파서 turn 에 물렸다. 거기는 툴 권한이
사람마다 갈리고 audit 의 `sub` 를 채워야 했기 때문이다. **여기는 익명 + 공개 데이터**라
토큰이 답할 질문이 하나뿐이다 — 「지금 도는 turn 인가」. 그래서 불투명 난수 하나면 된다.

## 저장은 해시, 폐기는 해시를 지우는 것

토큰 원문은 발급 즉시 codex 프로세스 인자로 흘러가고 back 은 붙들지 않는다. DB 에는
sha256 만 남고, 마감 때 그 칼럼을 NULL 로 만드는 것이 폐기다 — 별도 폐기 목록이 없으니
「폐기됐는데 아직 통과하는 창」도 없다.

## 검증 자리가 여기인 이유

MCP 서버는 어차피 back 의 chat-tool API 를 부른다. 그 요청에 Bearer 를 그대로 실어
보내면 **왕복 한 번으로 검증과 조회가 같이 끝난다** — 별도 verify 엔드포인트도,
MCP 쪽 폐기 캐시도 필요 없다. MCP 는 토큰이 아예 없는 호출만 자기 자리에서 막는다.

## 로그에 원문을 남기지 않는다 — **안 찍는 것**으로 한다

가리는 함수(mask·redact)를 두지 않는다. 그런 함수가 있으면 「가렸으니 찍어도 된다」가
되고, 실제로는 아무도 부르지 않는 죽은 코드로 남기 쉽다(리뷰 W3 — 발견 시점에 정확히
그 상태였다).

대신 토큰이 닿는 값을 **로그 인자로 만들지 않는다**. 토큰은 발급 직후 제출 인자
(`-c` 오버라이드의 `http_headers`)로 흘러가고 back 은 그것을 붙들지 않으며,
`runtime.start_turn` 의 성공·실패 로그는 둘 다 `message_id`·`task_id`·큐·모델만 찍는다
(그 자리에 경고 주석이 있다). 테스트가 이 성질을 단언한다.
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from dto.chat import ChatMessageDTO
from repository.chat_repo import ChatRepository, chat_repository


def hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class TurnTokenService:
    def __init__(self, repo: ChatRepository) -> None:
        self._repo = repo

    async def issue(self, session: AsyncSession, message_id: int) -> str:
        """이 assistant 메시지(=turn)에 토큰을 매단다. 반환은 **원문 한 번뿐**이다."""
        settings = get_settings()
        raw = secrets.token_urlsafe(32)
        await self._repo.update_message(
            session,
            message_id,
            {
                "turn_token_hash": hash_token(raw),
                "turn_token_expires_at": datetime.now(UTC)
                + timedelta(seconds=settings.chat_turn_token_ttl_sec),
            },
        )
        return raw

    async def verify(
        self, session: AsyncSession, raw: str | None
    ) -> ChatMessageDTO | None:
        """토큰이 가리키는 살아 있는 turn. 없으면 None — 이유는 구분하지 않는다."""
        if not raw:
            return None
        return await self._repo.find_by_turn_token(
            session, hash_token(raw), now=datetime.now(UTC)
        )

    async def revoke(self, session: AsyncSession, message_id: int) -> None:
        """마감 시 폐기. 해시를 지우면 그 토큰으로는 아무것도 못 찾는다."""
        await self._repo.update_message(
            session,
            message_id,
            {"turn_token_hash": None, "turn_token_expires_at": None},
        )


turn_token_service = TurnTokenService(chat_repository)
