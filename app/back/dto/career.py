"""역할(career) DTO — 내부 계층 이동용."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class CareerDTO:
    """career 행 + 회사 이름. is_current · period 는 여기 없다 — 표현은 schemas 가 한다."""

    id: int
    profile_id: int
    company_id: int
    company_name: str
    title: str
    started_on: date
    ended_on: date | None
    summary: str | None
    description: str | None
    stack: list[str] | None
