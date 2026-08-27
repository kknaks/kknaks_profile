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


@dataclass(frozen=True)
class PublicContentList:
    """공개 /contents 목록 — limit 적용된 항목 + 전체 행 수.

    totalCount 는 저장하지 않고 센다(erd §여기 두지 않는 것) — limit 로 잘라도
    전체 수는 그대로 내려간다.
    """

    items: list[ContentDTO]
    total_count: int


@dataclass(frozen=True)
class PublicContentDetail:
    """공개 /contents/{slug} 한 건 — 행 + md 전문 + 정렬 이웃.

    이전/다음 글은 컬럼이 아니다 — published_on 정렬의 이웃이다(erd §content).
    visible=true 만 이웃 대상이 된다.
    """

    dto: ContentDTO
    body: str
    newer: ContentDTO | None
    older: ContentDTO | None
