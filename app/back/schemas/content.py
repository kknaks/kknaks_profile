"""content — front ↔ back 계약. 어드민 콘텐츠(영상 + 교안) 화면이 읽고 쓴다.

profile_id 는 계약에 없다 — 1인 사이트라 서버가 첫 profile 로 채운다.
visible 은 어드민이라 거르지 않고 그대로 내려준다 — 공개 표면(/contents)이 거른다.
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from dto.content import ContentDTO, PublicContentDetail, PublicContentList


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


# ── 공개 /api/contents — lib/types.ts 의 ContentsResponse 와 1:1 ─────────────
#
# visible=false 는 service 가 걸렀다 — 응답에 visible 필드는 없다(erd §미결 3).
# detail_path 도 내리지 않는다 — 원장 경로는 서버 사정이다.
# subtitle·intro 는 내리지 않는다 — erd 에 대응 컬럼이 없고 프론트 기본 문구를 쓴다.


class PublicContentItem(BaseModel):
    id: int
    slug: str                                                   # C-025
    title: str
    summary: str | None = None
    youtube_id: str = Field(serialization_alias="youtubeId")
    duration: str | None = None                                 # 3:58
    speaker: str | None = None                                  # 출처 채널
    tags: list[str] = []
    published_on: date | None = Field(default=None, serialization_alias="publishedOn")

    @classmethod
    def from_dto(cls, dto: ContentDTO) -> PublicContentItem:
        return cls(
            id=dto.id,
            slug=dto.slug,
            title=dto.title,
            summary=dto.summary,
            youtube_id=dto.youtube_id,
            duration=dto.duration,
            speaker=dto.speaker,
            tags=dto.tags or [],
            published_on=dto.published_on,
        )


class PublicContentsMeta(BaseModel):
    total_count: int = Field(serialization_alias="totalCount")


class PublicContentsResponse(BaseModel):
    items: list[PublicContentItem] = Field(serialization_alias="contents[]")
    contents: PublicContentsMeta

    @classmethod
    def from_public(cls, result: PublicContentList) -> PublicContentsResponse:
        return cls(
            items=[PublicContentItem.from_dto(d) for d in result.items],
            contents=PublicContentsMeta(total_count=result.total_count),
        )


class PublicNeighbor(BaseModel):
    """이전/다음 글 — 컬럼이 아니라 published_on 정렬의 이웃(erd §content)."""

    slug: str
    title: str


class PublicContentDetailItem(PublicContentItem):
    """ContentItem + 본문 + 이웃 — lib/types.ts 의 ContentDetail 과 1:1.

    옛 frontmatter 의 concept[](요지 6문장)은 컬럼이 아니다 — 본문에 속하므로
    body 안에 있다(erd §content). 화면이 따로 조립하지 않는다.
    """

    body: str                                                   # detail_path md 전문
    newer: PublicNeighbor | None = None
    older: PublicNeighbor | None = None

    @classmethod
    def from_public(cls, detail: PublicContentDetail) -> PublicContentDetailItem:
        base = PublicContentItem.from_dto(detail.dto)
        return cls(
            **dict(base),
            body=detail.body,
            newer=PublicNeighbor(slug=detail.newer.slug, title=detail.newer.title)
            if detail.newer
            else None,
            older=PublicNeighbor(slug=detail.older.slug, title=detail.older.title)
            if detail.older
            else None,
        )


class PublicContentDetailResponse(BaseModel):
    detail: PublicContentDetailItem = Field(serialization_alias="contents.detail")
