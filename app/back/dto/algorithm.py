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


@dataclass(frozen=True)
class AlgorithmNeighbor:
    """이전/다음 회차 — 컬럼이 아니라 published_on 정렬의 이웃이다(erd.md §content 와 같은 규칙)."""

    slug: str
    title: str


@dataclass(frozen=True)
class PublicAlgorithmList:
    """공개 목록 한 벌 — visible 필터 후. today 는 그중 today=true 인 한 건(없으면 None)."""

    items: list[AlgorithmDTO]
    total_count: int
    today: AlgorithmDTO | None


@dataclass(frozen=True)
class PublicAlgorithmDetail:
    """공개 상세 한 벌 — 메타(dto) + 단계 구조 + 이웃.

    단계 구조는 컬럼이 아니다 — md 의 `## Data` fenced yaml 이 원천이고
    (erd.md §algorithm), service 가 계약 모양의 dict 로 정규화해 담는다.
    """

    dto: AlgorithmDTO
    problem: dict
    clarifying: dict
    approach: dict
    logic: dict
    trace: dict
    solution: dict
    newer: AlgorithmNeighbor | None
    older: AlgorithmNeighbor | None
