"""교육(education) DTO — 내부 계층 이동용."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class EducationDTO:
    """education 행 그대로. is_current · period 는 여기 없다 — 표현은 schemas 가 한다."""

    id: int
    profile_id: int
    org: str
    title: str
    location: str | None
    started_on: date
    ended_on: date | None
    summary: str | None
    detail_path: str | None
    stack: list[str] | None
