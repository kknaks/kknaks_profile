"""chat-tool DTO — AI 가 보는 이력 데이터의 모양.

목록과 상세가 **같은 필드 집합**을 쓴다(상세만 `body` 가 찬다). 모델이 tool 을 갈아탈
때 모양이 바뀌지 않아야 「목록에서 본 slug 를 상세에 넣는다」가 자연스럽다 —
tool 사슬을 설명 없이도 알게 하는 자리다(ai-agent: tool 은 용도가 새겨진 손).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ChatDocDTO:
    """이력 문서 한 건 — 목록의 한 줄이자 상세의 한 벌."""

    type: str                       # career | project | problem | note | content | algorithm
    slug: str
    title: str
    #: 제목 아래 한 줄 — 기간 · 조직 · 난이도처럼 「무엇인지」를 가르는 값.
    subtitle: str | None = None
    summary: str | None = None
    #: 상세 본문(md 또는 DB 컬럼). 목록에서는 항상 None 이다.
    body: str | None = None
    #: 그 유형에만 있는 값(stack · status · tags …). 없는 키는 두지 않는다.
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ChatProfileDTO:
    """`get_profile` — 이름 · 위치 · focus · stack · email (SPEC-017 §4 Tool Contract)."""

    name: str
    role: str
    years: str | None
    location: str | None
    focus: str | None
    email: str
    stack: list[str] = field(default_factory=list)
