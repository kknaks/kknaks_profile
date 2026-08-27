"""인박스(queue) DTO — 내부 계층 이동용."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class QueueDTO:
    """queue 행 그대로. 표현은 schemas 가 한다."""

    id: int
    kind: str
    source_url: str | None
    note: str | None
    status: str
    error: str | None
    ai_session_id: str | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class QueueList:
    """어드민 인박스 목록 — 최신순 항목 + 상태별 counts.

    counts 는 저장하지 않고 센다 — 목록과 같은 스냅샷에서 파생하므로
    화면의 항목과 어긋나지 않는다.
    """

    items: list[QueueDTO]
    counts: dict[str, int]
