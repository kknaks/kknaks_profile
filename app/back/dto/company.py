"""회사 DTO — 내부 계층 이동용."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class CompanyDTO:
    id: int
    slug: str
    name: str
    description: str | None
    location: str | None
    site: str | None
    logo_url: str | None


@dataclass(frozen=True)
class CompanyStatsDTO:
    """회사 + career 파생값. 재직 기간은 컬럼이 아니라 역할 행들의 최소·최대다(erd)."""

    company: CompanyDTO
    career_count: int
    started_on: date | None      # min(career.started_on)
    ended_on: date | None        # max(career.ended_on) — 현재 역할이 있으면 의미 없음
    is_current: bool             # any(career.ended_on IS NULL)
