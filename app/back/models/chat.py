"""채용담당자 채팅 — 익명 세션 · 대화 · 메시지 (SPEC-017 §4 Data Contract).

세 표가 1:N:N 으로 이어진다.

    chat_session (익명 방문자 1명)
      └─ conversation (대화 1건 = codex 세션 1개)
           └─ chat_message (질문/답변)

**세션과 대화를 가르는 이유**(DEC-026 D2): 한 방문자가 대화를 여러 개 만든다. AI 세션
참조(`ai_session_id`)는 conversation 이 갖는다 — 대화 하나가 codex 세션 하나다.

**신원은 담지 않는다**(DEC-026 D3). 남는 것은 대화 내용과 시각뿐이고, 쿠키 원문도 두지
않는다 — 해시만 있으면 검증이 되고, DB 가 새도 쿠키를 복원할 수 없다.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin

# role · status 는 CHECK 가 아니라 짧은 문자열이다 — 이 레포의 다른 표(project.status ·
# algorithm.difficulty)와 같은 규약이다. 값의 정본은 이 상수들이다.
ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"

STATUS_PENDING = "pending"
STATUS_DONE = "done"
STATUS_FAILED = "failed"


class ChatSession(Base, TimestampMixin):
    """익명 방문자 1명. 외부 노출 없음 — 쿠키가 유일한 손잡이다(DEC-026 D1)."""

    __tablename__ = "chat_session"

    id: Mapped[int] = mapped_column(primary_key=True)

    # 쿠키 값(UUID)의 sha256 hex. 원문을 두지 않는 이유는 머리 주석 참조.
    token_hash: Mapped[str] = mapped_column(String(64), unique=True)

    # 만료는 30일 sliding — 요청마다 여기를 밀어 올린다(DEC-026 D1).
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Conversation(Base, TimestampMixin):
    """대화 1건. `ai_session_id` 는 내부 필드다 — 공개 응답에 싣지 않는다(SPEC-017 §4)."""

    __tablename__ = "conversation"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("chat_session.id", ondelete="CASCADE")
    )

    # 첫 질문에서 딴다(최대 50자 — SPEC-017 U-4). 잘림 표시는 화면이 한다.
    title: Mapped[str] = mapped_column(String(64))

    # codex `result_session_id`. 다음 질문이 resume 으로 넘긴다(DEC-027 D2).
    # 없거나 죽었으면 새 세션으로 간다 — 실패시키지 않는다.
    ai_session_id: Mapped[str | None] = mapped_column(String(128))

    __table_args__ = (
        # 사이드바는 이 세션의 대화를 최신순으로 읽는다.
        # `created_at` 은 TimestampMixin 이 갖고 있어 클래스 본문에 이름이 없다 —
        # 그래서 컬럼 객체가 아니라 SQL 표현으로 적는다.
        Index("ix_conversation_session", session_id, text("created_at DESC")),
    )


class ChatMessage(Base, TimestampMixin):
    """질문 한 줄 또는 답변 한 덩어리.

    답변은 **먼저 `pending` 으로 만들어지고** 소비자가 이벤트를 폴딩하며 자란다
    (SPEC-017 §4 «pending 중에도 content·steps 가 채워진다»). 그래서 `content` 는
    부분 텍스트이기도 하고 최종 본문이기도 하다 — `status` 가 어느 쪽인지 말한다.
    """

    __tablename__ = "chat_message"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversation.id", ondelete="CASCADE")
    )

    role: Mapped[str] = mapped_column(String(16))                       # user / assistant
    # user 메시지는 만들어질 때 이미 done 이다 — 질문은 자라지 않는다.
    status: Mapped[str] = mapped_column(String(16), server_default=STATUS_DONE)
    content: Mapped[str] = mapped_column(Text, server_default="")

    # 근거 카드 — [{type, slug, title, url}]. 소비자가 문서 계열 tool_result 에서 뽑는다
    # (AI 의 자기 신고가 아니라 실제로 읽은 것 — SPEC-017 S-9 2항).
    sources: Mapped[list[dict[str, Any]] | None] = mapped_column(JSONB)
    # tool 단계 — [{toolUseId, tool, argsSummary, durationMs, calledAt, status}].
    # 공개 응답은 이 중 spec §4 의 네 필드만 싣는다(schemas/chat.py).
    steps: Mapped[list[dict[str, Any]] | None] = mapped_column(JSONB)

    # ── 소비자·복구가 쓰는 내부 필드 (공개 응답에 없다) ─────────────
    # open-kknaks task id. 기동 스윕이 이걸로 스트림에 다시 붙는다.
    task_id: Mapped[str | None] = mapped_column(String(64))
    # AI_FAILED / AI_TIMEOUT — spec §4 Case Matrix 의 「code 만 구분」.
    error_code: Mapped[str | None] = mapped_column(String(32))
    # turn 전용 MCP Bearer 토큰의 sha256. 마감 때 NULL 로 지우는 것이 폐기다(DEC-027 D5).
    turn_token_hash: Mapped[str | None] = mapped_column(String(64))
    turn_token_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    __table_args__ = (
        Index("ix_chat_message_conversation", conversation_id, id),
        # **직렬화를 DB 가 강제한다**(SPEC-017 §5 · WORK-023 invariant): 한 대화에
        # pending assistant 는 최대 하나다. 앱의 409 검사가 새는 경로(동시 요청)를
        # 여기서 막는다 — algorithm.today 의 partial unique index 와 같은 손잡이다.
        Index(
            "uq_chat_message_pending",
            conversation_id,
            unique=True,
            postgresql_where=text(
                f"status = '{STATUS_PENDING}' AND role = '{ROLE_ASSISTANT}'"
            ),
        ),
        # turn 토큰 검증은 매 tool 호출마다 돈다 — 해시로 바로 찾는다.
        Index("ix_chat_message_turn_token", turn_token_hash),
    )
