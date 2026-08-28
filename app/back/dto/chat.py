"""채팅 DTO — 내부 계층 이동용. ORM 은 repository 를 넘지 않는다."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
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
