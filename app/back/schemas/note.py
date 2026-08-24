"""note — front ↔ back 계약. 어드민 노트 화면이 읽고 쓴다.

profile_id 는 계약에 없다 — 1인 사이트라 서버가 첫 profile 로 채운다.
visible 은 어드민이라 거르지 않고 그대로 내려준다 — 공개 표면이 서면 그쪽이 거른다.
"""

from __future__ import annotations

import datetime
from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from dto.note import NoteDTO, NoteFileDTO


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
