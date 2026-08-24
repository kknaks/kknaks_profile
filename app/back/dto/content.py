"""콘텐츠(content) DTO — 내부 계층 이동용."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ContentDTO:
    """content 행 그대로. 표현은 schemas 가 한다."""

    id: int
    profile_id: int
    slug: str
    title: str
    summary: str | None
    detail_path: str
    youtube_id: str
    duration: str | None
    speaker: str | None
    tags: list[str] | None
    published_on: date | None
    visible: bool
