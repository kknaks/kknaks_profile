"""activity DTO — 내부 계층 이동용.

테이블이 없다 — commit 을 날짜로 묶은 파생이다(erd.md §잔디).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ActivityDayDTO:
    day: date
    count: int
    summaries: list[str]                # daily.summary 불릿. 미요약·error 면 빈 배열


@dataclass(frozen=True)
class ActivityDTO:
    days: list[ActivityDayDTO]
    total_count: int                    # 창(지난 1년) 안의 커밋 수 합
    since: date
    until: date
