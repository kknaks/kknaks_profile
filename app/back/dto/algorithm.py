"""알고리즘(algorithm) DTO — 내부 계층 이동용."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class AlgorithmDTO:
    """algorithm 행 그대로. 표현은 schemas 가 한다."""

    id: int
    profile_id: int
    slug: str
    title: str
    difficulty: str
    summary: str | None
    source_platform: str
    source_number: int | None
    source_url: str | None
    curated_in: list[str] | None
    tags: list[str] | None
    today: bool
    detail_path: str
    published_on: date | None
    visible: bool
