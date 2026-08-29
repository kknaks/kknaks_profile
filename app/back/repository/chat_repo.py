"""chat_session · conversation · chat_message 표 접근 — 3층.

ORM 은 여기를 넘지 않는다. 위층은 DTO 만 본다 — 단, **소비자는 예외**다:
이벤트 폴딩은 같은 row 를 수십 번 갱신하므로 dto 왕복이 낭비다. 그래서 소비자가 쓰는
메서드만 «필드 patch» 형태로 두고(`update_message`), ORM 객체를 밖으로 내보내지 않는다.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from sqlalchemy import Date, case, cast, column, func, select, true, update
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession

from dto.chat import (
    AdminConversationDTO,
    ChatMessageDTO,
    ConversationDTO,
    DailyQuestionDTO,
    RecentQuestionDTO,
    TopSourceDTO,
)
from models.chat import (
    ROLE_ASSISTANT,
    ROLE_USER,
    STATUS_PENDING,
    ChatMessage,
    ChatSession,
    Conversation,
)

# 날짜 집계의 기준 시간대. DB 세션 TZ 에 기대지 않고 식에 못박는다 —
# `commit_repo` 의 어드민 달력과 같은 규약이다.
_KST = "Asia/Seoul"


def _kst_day():
    """`chat_message.created_at` 의 KST 날짜."""
    return cast(func.timezone(_KST, ChatMessage.created_at), Date)


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

    # ── 어드민 열람·인사이트 (U-8 · WORK-025) ────────────
    async def list_conversations_page(
        self, session: AsyncSession, *, limit: int, offset: int
    ) -> tuple[list[AdminConversationDTO], int]:
        """세션을 가리지 않는 한 페이지 + 전체 건수.

        정렬은 **`created_at DESC, id DESC`** — 방문자 사이드바(`list_conversations`)와
        같은 「최신순」이다. 「최근 메시지순」으로 바꾸면 오래된 대화가 새 질문 하나로
        맨 위에 올라와 페이지 경계가 요청 사이에 흔들린다.

        메시지 수 · 최근 시각은 집계 서브쿼리로 한 번에 붙인다 — 페이지당 N+1 조회를
        만들지 않는다. 메시지가 없는 대화(있을 수 없지만)는 `last_message_at` 이
        대화 생성 시각으로 떨어진다.
        """
        agg = (
            select(
                ChatMessage.conversation_id.label("conversation_id"),
                func.count(ChatMessage.id).label("message_count"),
                func.max(ChatMessage.created_at).label("last_message_at"),
            )
            .group_by(ChatMessage.conversation_id)
            .subquery()
        )
        total = (
            await session.execute(select(func.count()).select_from(Conversation))
        ).scalar_one()
        rows = (
            await session.execute(
                select(
                    Conversation,
                    func.coalesce(agg.c.message_count, 0),
                    func.coalesce(agg.c.last_message_at, Conversation.created_at),
                )
                .outerjoin(agg, agg.c.conversation_id == Conversation.id)
                .order_by(Conversation.created_at.desc(), Conversation.id.desc())
                .limit(limit)
                .offset(offset)
            )
        ).all()
        return [
            AdminConversationDTO(
                id=row[0].id,
                session_id=row[0].session_id,
                title=row[0].title,
                message_count=row[1],
                created_at=row[0].created_at,
                last_message_at=row[2],
            )
            for row in rows
        ], total

    async def count_conversations(self, session: AsyncSession) -> int:
        return (
            await session.execute(select(func.count()).select_from(Conversation))
        ).scalar_one()

    async def count_questions(
        self, session: AsyncSession, *, since_day: date | None = None
    ) -> int:
        """질문(user 메시지) 수. `since_day` 를 주면 그 KST 날짜부터 센다."""
        stmt = select(func.count()).select_from(ChatMessage).where(
            ChatMessage.role == ROLE_USER
        )
        if since_day is not None:
            stmt = stmt.where(_kst_day() >= since_day)
        return (await session.execute(stmt)).scalar_one()

    async def recent_questions(
        self, session: AsyncSession, *, limit: int
    ) -> list[RecentQuestionDTO]:
        """최근 질문 피드 — 최신순(U-8 위젯 ①)."""
        rows = (
            await session.execute(
                select(
                    ChatMessage.content,
                    ChatMessage.created_at,
                    ChatMessage.conversation_id,
                )
                .where(ChatMessage.role == ROLE_USER)
                .order_by(ChatMessage.created_at.desc(), ChatMessage.id.desc())
                .limit(limit)
            )
        ).all()
        return [
            RecentQuestionDTO(question=r[0], asked_at=r[1], conversation_id=r[2])
            for r in rows
        ]

    async def daily_questions(
        self, session: AsyncSession, *, since_day: date
    ) -> list[DailyQuestionDTO]:
        """KST 날짜별 질문 수 — **있는 날만** 돌려준다.

        빈 날 채우기는 서비스가 한다. 여기서 채우려면 날짜 시리즈를 SQL 로 만들어야
        하는데, 30칸을 파이썬에서 채우는 편이 읽기 쉽고 결과가 같다.
        """
        day = _kst_day()
        rows = (
            await session.execute(
                select(day.label("day"), func.count().label("count"))
                .where(ChatMessage.role == ROLE_USER, day >= since_day)
                .group_by(day)
                .order_by(day)
            )
        ).all()
        return [DailyQuestionDTO(day=r[0], count=r[1]) for r in rows]

    async def top_sources(
        self, session: AsyncSession, *, limit: int
    ) -> list[TopSourceDTO]:
        """근거로 많이 읽힌 문서 Top N — assistant 메시지의 `sources` jsonb 를 전개해 센다.

        같은 문서가 한 답변 안에 두 번 실리면 두 번 센다 — 「몇 번 근거로 실렸나」가
        세는 대상이고, 소비자 폴딩이 중복을 만들지 않는다(멱등 upsert).

        동수일 때는 `type` · `slug` 순으로 갈라 결과를 결정적으로 만든다 — 안 그러면
        같은 데이터에 매 요청 다른 Top 이 나온다.

        **배열이 아닌 값은 join 안에서 빈 배열로 접는다.** `sources` 에 파이썬 `None` 을
        넣으면 SQL NULL 이 아니라 **JSONB `'null'`** 이 저장되고(JSONB 기본 동작 —
        재시도가 `sources: None` 으로 초기화하는 경로가 실제로 그렇다),
        `jsonb_array_elements('null')` 는 「cannot extract elements from a scalar」로
        터진다. WHERE 로는 못 막는다 — LATERAL 은 WHERE 보다 먼저 돈다.
        """
        elem = (
            func.jsonb_array_elements(
                case(
                    (
                        func.jsonb_typeof(ChatMessage.sources) == "array",
                        ChatMessage.sources,
                    ),
                    else_=func.jsonb_build_array(),
                )
            )
            .table_valued(column("value", JSONB))
            .lateral()
        )
        type_ = elem.c.value["type"].astext
        slug_ = elem.c.value["slug"].astext
        title_ = elem.c.value["title"].astext
        rows = (
            await session.execute(
                select(
                    type_.label("type"),
                    slug_.label("slug"),
                    title_.label("title"),
                    func.count().label("count"),
                )
                .select_from(ChatMessage)
                .join(elem, true())
                .where(ChatMessage.role == ROLE_ASSISTANT)
                .group_by(type_, slug_, title_)
                .order_by(func.count().desc(), type_, slug_)
                .limit(limit)
            )
        ).all()
        return [
            TopSourceDTO(
                type=r[0] or "", slug=r[1] or "", title=r[2] or "", count=r[3]
            )
            for r in rows
        ]

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
