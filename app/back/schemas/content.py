"""content — front ↔ back 계약. 어드민 콘텐츠(영상 + 교안) 화면이 읽고 쓴다.

profile_id 는 계약에 없다 — 1인 사이트라 서버가 첫 profile 로 채운다.
visible 은 어드민이라 거르지 않고 그대로 내려준다 — 공개 표면(/contents)이 거른다.
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from dto.content import ContentDTO


class AdminContentItem(BaseModel):
    id: int
    slug: str
    title: str
    summary: str | None = None
    detail_path: str = Field(serialization_alias="detailPath")
    youtube_id: str = Field(serialization_alias="youtubeId")
    duration: str | None = None
    speaker: str | None = None
    tags: list[str] = []
    published_on: date | None = Field(default=None, serialization_alias="publishedOn")
    visible: bool

    @classmethod
    def from_dto(cls, dto: ContentDTO) -> AdminContentItem:
        return cls(
            id=dto.id,
            slug=dto.slug,
            title=dto.title,
            summary=dto.summary,
            detail_path=dto.detail_path,
            youtube_id=dto.youtube_id,
            duration=dto.duration,
            speaker=dto.speaker,
            tags=dto.tags or [],
            published_on=dto.published_on,
            visible=dto.visible,
        )


class AdminContentsResponse(BaseModel):
    items: list[AdminContentItem]


class ContentCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    slug: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=128)
    summary: str | None = None
    detail_path: str = Field(
        min_length=1, max_length=255, validation_alias="detailPath"
    )
    youtube_id: str = Field(
        min_length=1, max_length=16, validation_alias="youtubeId"
    )
    duration: str | None = Field(default=None, max_length=16)
    speaker: str | None = Field(default=None, max_length=64)
    tags: list[str] | None = None
    published_on: date | None = Field(default=None, validation_alias="publishedOn")
    visible: bool = True


class ContentUpdate(BaseModel):
    """PATCH body — 보낸 필드만 반영 (exclude_unset). NOT NULL 에 null 은 service 가 422."""

    model_config = ConfigDict(populate_by_name=True)

    slug: str | None = Field(default=None, min_length=1, max_length=64)
    title: str | None = Field(default=None, min_length=1, max_length=128)
    summary: str | None = None
    detail_path: str | None = Field(
        default=None, max_length=255, validation_alias="detailPath"
    )
    youtube_id: str | None = Field(
        default=None, max_length=16, validation_alias="youtubeId"
    )
    duration: str | None = Field(default=None, max_length=16)
    speaker: str | None = Field(default=None, max_length=64)
    tags: list[str] | None = None
    published_on: date | None = Field(default=None, validation_alias="publishedOn")
    visible: bool | None = None
