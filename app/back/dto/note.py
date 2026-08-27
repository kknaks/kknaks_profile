"""노트(note) DTO — 내부 계층 이동용."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class NoteDTO:
    """note 행 그대로. 표현은 schemas 가 한다."""

    id: int
    profile_id: int
    slug: str
    title: str
    summary: str | None
    detail_path: str
    tags: list[str] | None
    published_on: date | None
    visible: bool


@dataclass(frozen=True)
class NoteNeighbor:
    """이전/다음 글 — **컬럼이 아니다.** published_on 정렬의 이웃이다(erd.md §content)."""

    slug: str
    title: str


@dataclass(frozen=True)
class PublicNoteList:
    """공개 목록 한 벌 — visible=true 만 담고, total_count 는 자르기 전 전체 수."""

    items: list[NoteDTO]
    total_count: int


@dataclass(frozen=True)
class PublicNoteDetail:
    """공개 상세 한 벌 — 행 + md 전문 + 정렬 이웃."""

    dto: NoteDTO
    body: str
    newer: NoteNeighbor | None
    older: NoteNeighbor | None


@dataclass(frozen=True)
class NoteFileDTO:
    """등록 후보 md 파일 — para/resources/note/ 의 미등록 파일 하나.

    DB 행이 아니라 파일시스템 + frontmatter 에서 뽑은 값이다. 폼 프리필용.
    """

    path: str            # repo 루트 기준 상대경로 — para/resources/note/...
    stem: str            # 파일명 stem — slug 프리필 후보
    title: str | None
    summary: str | None
    date: date | None    # frontmatter date — publishedOn 프리필
    tags: list[str] | None
