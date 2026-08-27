"""note — front ↔ back 계약. 어드민 노트 화면 + 공개 /notes.

profile_id 는 계약에 없다 — 1인 사이트라 서버가 첫 profile 로 채운다.
visible 은 어드민만 그대로 내려준다 — 공개 응답은 service 가 걸러서 필드 자체가 없다.
"""

from __future__ import annotations

import datetime
from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from dto.note import NoteDTO, NoteFileDTO, NoteNeighbor, PublicNoteDetail, PublicNoteList


class AdminNoteItem(BaseModel):
    id: int
    slug: str
    title: str
    summary: str | None = None
    detail_path: str = Field(serialization_alias="detailPath")
    tags: list[str] = []
    published_on: date | None = Field(default=None, serialization_alias="publishedOn")
    visible: bool

    @classmethod
    def from_dto(cls, dto: NoteDTO) -> AdminNoteItem:
        return cls(
            id=dto.id,
            slug=dto.slug,
            title=dto.title,
            summary=dto.summary,
            detail_path=dto.detail_path,
            tags=dto.tags or [],
            published_on=dto.published_on,
            visible=dto.visible,
        )


class AdminNotesResponse(BaseModel):
    items: list[AdminNoteItem]


class NoteFileItem(BaseModel):
    """등록 후보 파일 — DB 행이 아니라 frontmatter 에서 뽑은 프리필 값이다."""

    path: str
    stem: str
    title: str | None = None
    summary: str | None = None
    # 필드명이 타입명과 겹쳐서 모듈 경로로 적는다 — `date: date` 는 평가가 깨진다.
    date: datetime.date | None = None
    tags: list[str] = []

    @classmethod
    def from_dto(cls, dto: NoteFileDTO) -> NoteFileItem:
        return cls(
            path=dto.path,
            stem=dto.stem,
            title=dto.title,
            summary=dto.summary,
            date=dto.date,
            tags=dto.tags or [],
        )


class NoteFilesResponse(BaseModel):
    items: list[NoteFileItem]


class NoteCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    slug: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=128)
    summary: str | None = None
    detail_path: str = Field(
        min_length=1, max_length=255, validation_alias="detailPath"
    )
    tags: list[str] | None = None
    published_on: date | None = Field(default=None, validation_alias="publishedOn")
    visible: bool = True


# ── 공개 /api/notes — lib/types.ts 의 NotesResponse 와 1:1 ──────────────────
#
# visible=false 는 service 가 걸렀다 — 응답에 visible 필드는 없다(erd §미결 3).
# subtitle 은 내리지 않는다 — erd 에 대응 컬럼이 없고 프론트 기본 문구를 쓴다.

_NOTE_PREFIX = "para/resources/note/"


def _note_folder(detail_path: str) -> str:
    """detail_path 의 note/ 이하 첫 디렉토리 — **컬럼이 아니라 경로의 파생**이다.

    원장이 8개 폴더(backend·bitcamp·…)로 나뉘어 있고, 디렉토리 트리 UI 가
    이 값으로 묶는다. 폴더 없이 note/ 바로 아래 놓인 파일이면 빈 문자열.
    """
    rel = detail_path.removeprefix(_NOTE_PREFIX)
    return rel.split("/", 1)[0] if "/" in rel else ""


class PublicNoteItem(BaseModel):
    id: int
    slug: str
    title: str
    summary: str | None = None
    tags: list[str] = []
    published_on: date | None = Field(default=None, serialization_alias="publishedOn")
    folder: str                                                 # detail_path 파생

    @classmethod
    def from_dto(cls, dto: NoteDTO) -> PublicNoteItem:
        return cls(
            id=dto.id,
            slug=dto.slug,
            title=dto.title,
            summary=dto.summary,
            tags=dto.tags or [],
            published_on=dto.published_on,
            folder=_note_folder(dto.detail_path),
        )


class PublicNotesMeta(BaseModel):
    total_count: int = Field(serialization_alias="totalCount")


class PublicNotesResponse(BaseModel):
    items: list[PublicNoteItem] = Field(serialization_alias="notes[]")
    notes: PublicNotesMeta

    @classmethod
    def from_bundle(cls, bundle: PublicNoteList) -> PublicNotesResponse:
        return cls(
            items=[PublicNoteItem.from_dto(d) for d in bundle.items],
            notes=PublicNotesMeta(total_count=bundle.total_count),
        )


class PublicNoteNeighbor(BaseModel):
    """이전/다음 글 — 컬럼이 아니라 published_on 정렬의 이웃이다(erd.md)."""

    slug: str
    title: str

    @classmethod
    def from_dto(cls, dto: NoteNeighbor | None) -> PublicNoteNeighbor | None:
        return cls(slug=dto.slug, title=dto.title) if dto else None


class PublicNoteDetailItem(PublicNoteItem):
    body: str                                                   # detail_path md 전문
    newer: PublicNoteNeighbor | None = None
    older: PublicNoteNeighbor | None = None

    @classmethod
    def from_public(cls, detail: PublicNoteDetail) -> PublicNoteDetailItem:
        base = PublicNoteItem.from_dto(detail.dto)
        return cls(
            **base.model_dump(),
            body=detail.body,
            newer=PublicNoteNeighbor.from_dto(detail.newer),
            older=PublicNoteNeighbor.from_dto(detail.older),
        )


class PublicNoteDetailResponse(BaseModel):
    detail: PublicNoteDetailItem = Field(serialization_alias="notes.detail")


class NoteUpdate(BaseModel):
    """PATCH body — 보낸 필드만 반영 (exclude_unset). NOT NULL 에 null 은 service 가 422."""

    model_config = ConfigDict(populate_by_name=True)

    slug: str | None = Field(default=None, min_length=1, max_length=64)
    title: str | None = Field(default=None, min_length=1, max_length=128)
    summary: str | None = None
    detail_path: str | None = Field(
        default=None, max_length=255, validation_alias="detailPath"
    )
    tags: list[str] | None = None
    published_on: date | None = Field(default=None, validation_alias="publishedOn")
    visible: bool | None = None
