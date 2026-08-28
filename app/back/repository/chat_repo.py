"""chat_session · conversation · chat_message 표 접근 — 3층.

ORM 은 여기를 넘지 않는다. 위층은 DTO 만 본다 — 단, **소비자는 예외**다:
이벤트 폴딩은 같은 row 를 수십 번 갱신하므로 dto 왕복이 낭비다. 그래서 소비자가 쓰는
메서드만 «필드 patch» 형태로 두고(`update_message`), ORM 객체를 밖으로 내보내지 않는다.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from dto.chat import ChatMessageDTO, ConversationDTO
from models.chat import (
    ROLE_ASSISTANT,
    STATUS_PENDING,
    ChatMessage,
    ChatSession,
    Conversation,
)


def _conversation_dto(row: Conversation) -> ConversationDTO:
    return ConversationDTO(
        id=row.id,
        session_id=row.session_id,
        title=row.title,
        created_at=row.created_at,
        ai_session_id=row.ai_session_id,
    )


def _message_dto(row: ChatMessage) -> ChatMessageDTO:
    return ChatMessageDTO(
        id=row.id,
        conversation_id=row.conversation_id,
        role=row.role,
        status=row.status,
        content=row.content or "",
        created_at=row.created_at,
        sources=list(row.sources or []),
        steps=list(row.steps or []),
        task_id=row.task_id,
        error_code=row.error_code,
    )


class ChatRepository:
    # ── 세션 ────────────────────────────────────────────
    async def get_session_id(
        self, session: AsyncSession, token_hash: str, *, not_before: datetime
    ) -> int | None:
        """살아 있는 세션만 찾는다 — `last_seen_at` 이 `not_before` 보다 오래면 없는 것이다.

        만료 컷을 **쿼리 안에** 두는 이유: 조회한 뒤 파이썬에서 거르면 「찾았지만
        만료」라는 중간 상태가 생기고, 그 상태를 어디서 처리할지가 호출부마다 갈린다.
        여기서 못 찾으면 그냥 새 손님이다(DEC-026 D1 — 복구 수단은 없다).
        """
        return await session.scalar(
            select(ChatSession.id).where(
                ChatSession.token_hash == token_hash,
                ChatSession.last_seen_at > not_before,
            )
        )

    async def create_session(self, session: AsyncSession, token_hash: str) -> int:
        row = ChatSession(token_hash=token_hash)
        session.add(row)
        await session.flush()
        return row.id

    async def touch_session(
        self, session: AsyncSession, session_id: int, *, now: datetime
    ) -> None:
        """마지막 사용 시각 갱신 — 30일 sliding 만료의 실체(DEC-026 D1)."""
        await session.execute(
            update(ChatSession)
            .where(ChatSession.id == session_id)
            .values(last_seen_at=now)
        )

    # ── 대화 ────────────────────────────────────────────
    async def list_conversations(
        self, session: AsyncSession, session_id: int
    ) -> list[ConversationDTO]:
        """이 세션의 대화 — 최신순(U-4 사이드바)."""
        rows = (
            (
                await session.execute(
                    select(Conversation)
                    .where(Conversation.session_id == session_id)
                    .order_by(Conversation.created_at.desc(), Conversation.id.desc())
                )
            )
            .scalars()
            .all()
        )
        return [_conversation_dto(row) for row in rows]

    async def get_conversation(
        self, session: AsyncSession, conversation_id: int
    ) -> ConversationDTO | None:
        row = await session.get(Conversation, conversation_id)
        return _conversation_dto(row) if row else None

    async def create_conversation(
        self, session: AsyncSession, *, session_id: int, title: str
    ) -> ConversationDTO:
        row = Conversation(session_id=session_id, title=title)
        session.add(row)
        await session.flush()
        return _conversation_dto(row)

    async def set_ai_session_id(
        self, session: AsyncSession, conversation_id: int, ai_session_id: str
    ) -> None:
        await session.execute(
            update(Conversation)
            .where(Conversation.id == conversation_id)
            .values(ai_session_id=ai_session_id)
        )

    # ── 메시지 ──────────────────────────────────────────
    async def list_messages(
        self, session: AsyncSession, conversation_id: int
    ) -> list[ChatMessageDTO]:
        rows = (
            (
                await session.execute(
                    select(ChatMessage)
                    .where(ChatMessage.conversation_id == conversation_id)
                    .order_by(ChatMessage.id.asc())
                )
            )
            .scalars()
            .all()
        )
        return [_message_dto(row) for row in rows]

    async def get_message(
        self, session: AsyncSession, message_id: int
    ) -> ChatMessageDTO | None:
        row = await session.get(ChatMessage, message_id)
        return _message_dto(row) if row else None

    async def create_message(
        self, session: AsyncSession, fields: dict[str, Any]
    ) -> ChatMessageDTO:
        row = ChatMessage(**fields)
        session.add(row)
        await session.flush()
        return _message_dto(row)

    async def update_message(
        self, session: AsyncSession, message_id: int, fields: dict[str, Any]
    ) -> ChatMessageDTO | None:
        """보낸 필드만 얹는다. 소비자 폴딩이 매 이벤트마다 부른다."""
        row = await session.get(ChatMessage, message_id)
        if row is None:
            return None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        return _message_dto(row)

    async def pending_count(self, session: AsyncSession, conversation_id: int) -> int:
        """이 대화의 pending assistant 수 — 409 판정용(SPEC-017 §5 직렬화).

        DB 의 partial unique index 가 최종 방어선이고, 이건 그 앞에서 친절한 409 를
        내기 위한 검사다.
        """
        return (
            await session.execute(
                select(func.count(ChatMessage.id)).where(
                    ChatMessage.conversation_id == conversation_id,
                    ChatMessage.role == ROLE_ASSISTANT,
                    ChatMessage.status == STATUS_PENDING,
                )
            )
        ).scalar_one()

    async def list_pending_messages(
        self, session: AsyncSession
    ) -> list[ChatMessageDTO]:
        """기동 시 스윕 대상 — 아직 pending 인 assistant 전부(WORK-023 P4)."""
        rows = (
            (
                await session.execute(
                    select(ChatMessage).where(
                        ChatMessage.role == ROLE_ASSISTANT,
                        ChatMessage.status == STATUS_PENDING,
                    )
                )
            )
            .scalars()
            .all()
        )
        return [_message_dto(row) for row in rows]

    # ── turn 토큰 ───────────────────────────────────────
    async def find_by_turn_token(
        self, session: AsyncSession, token_hash: str, *, now: datetime
    ) -> ChatMessageDTO | None:
        """살아 있는 turn 토큰 하나 — 만료·폐기(해시 NULL)면 안 잡힌다.

        폐기가 «해시를 지우는 것» 이라 폐기된 토큰은 여기서 구조적으로 못 찾는다 —
        별도 폐기 목록을 두지 않는 이유다.
        """
        row = (
            await session.execute(
                select(ChatMessage).where(
                    ChatMessage.turn_token_hash == token_hash,
                    ChatMessage.turn_token_expires_at > now,
                )
            )
        ).scalar_one_or_none()
        return _message_dto(row) if row else None


chat_repository = ChatRepository()
