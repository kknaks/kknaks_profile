"""채팅 DTO — 내부 계층 이동용. ORM 은 repository 를 넘지 않는다."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any


@dataclass(frozen=True)
class ConversationDTO:
    id: int
    session_id: int
    title: str
    created_at: datetime
    # 내부 필드 — 공개 응답에 싣지 않는다(SPEC-017 §4 Data Contract).
    ai_session_id: str | None = None


@dataclass(frozen=True)
class ChatMessageDTO:
    id: int
    conversation_id: int
    role: str
    status: str
    content: str
    created_at: datetime
    sources: list[dict[str, Any]] = field(default_factory=list)
    steps: list[dict[str, Any]] = field(default_factory=list)
    # 내부 — 소비자·복구가 쓴다. schemas 가 내려주지 않는다.
    task_id: str | None = None
    error_code: str | None = None


@dataclass(frozen=True)
class ConversationBundle:
    """대화 한 벌 — 폴링이 매번 받는 것 전부."""

    conversation: ConversationDTO
    messages: list[ChatMessageDTO]


# ── 어드민 열람·인사이트 (SPEC-017 §2 U-8 · WORK-025) ────
@dataclass(frozen=True)
class AdminConversationDTO:
    """어드민 목록 한 줄 — 방문자 목록에 없는 세션 id · 메시지 수 · 최근 시각이 붙는다."""

    id: int
    session_id: int
    title: str
    message_count: int
    created_at: datetime
    last_message_at: datetime


@dataclass(frozen=True)
class AdminConversationPageDTO:
    items: list[AdminConversationDTO]
    total: int
    page: int
    size: int


@dataclass(frozen=True)
class RecentQuestionDTO:
    question: str
    asked_at: datetime
    conversation_id: int


@dataclass(frozen=True)
class DailyQuestionDTO:
    """하루치 질문 수. 날짜는 KST(어드민 커밋 달력과 같은 기준)."""

    day: date
    count: int


@dataclass(frozen=True)
class TopSourceDTO:
    type: str
    slug: str
    title: str
    count: int


@dataclass(frozen=True)
class ChatInsightsDTO:
    """위젯 3종이 한 번에 받는 것 — 전부 요청 시 계산이다(사전 집계 표 없음)."""

    conversations: int
    questions: int
    last7d: int
    recent_questions: list[RecentQuestionDTO]
    daily: list[DailyQuestionDTO]
    top_sources: list[TopSourceDTO]
