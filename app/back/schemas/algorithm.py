"""algorithm — front ↔ back 계약. 어드민 알고리즘 화면이 읽고 쓴다.

메타만 다룬다 — 본문 단계(Problem→…→Solution)는 detail_path 의 md 몫이다.
profile_id 는 계약에 없다 — 1인 사이트라 서버가 첫 profile 로 채운다.
visible 은 어드민이라 거르지 않고 그대로 내려준다.
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from dto.algorithm import AlgorithmDTO


class AdminAlgorithmItem(BaseModel):
    id: int
    slug: str
    title: str
    difficulty: str
    summary: str | None = None
    source_platform: str = Field(serialization_alias="sourcePlatform")
    source_number: int | None = Field(default=None, serialization_alias="sourceNumber")
    source_url: str | None = Field(default=None, serialization_alias="sourceUrl")
    curated_in: list[str] = Field(default=[], serialization_alias="curatedIn")
    tags: list[str] = []
    today: bool
    detail_path: str = Field(serialization_alias="detailPath")
    published_on: date | None = Field(default=None, serialization_alias="publishedOn")
    visible: bool

    @classmethod
    def from_dto(cls, dto: AlgorithmDTO) -> AdminAlgorithmItem:
        return cls(
            id=dto.id,
            slug=dto.slug,
            title=dto.title,
            difficulty=dto.difficulty,
            summary=dto.summary,
            source_platform=dto.source_platform,
            source_number=dto.source_number,
            source_url=dto.source_url,
            curated_in=dto.curated_in or [],
            tags=dto.tags or [],
            today=dto.today,
            detail_path=dto.detail_path,
            published_on=dto.published_on,
            visible=dto.visible,
        )


class AdminAlgorithmsResponse(BaseModel):
    items: list[AdminAlgorithmItem]


class AlgorithmCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    slug: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=128)
    # easy/medium/hard 검사는 service 가 한다 — 422 문구를 한 곳에서 내려고.
    difficulty: str = Field(min_length=1, max_length=8)
    summary: str | None = None
    source_platform: str = Field(
        min_length=1, max_length=32, validation_alias="sourcePlatform"
    )
    source_number: int | None = Field(default=None, validation_alias="sourceNumber")
    source_url: str | None = Field(
        default=None, max_length=255, validation_alias="sourceUrl"
    )
    curated_in: list[str] | None = Field(default=None, validation_alias="curatedIn")
    tags: list[str] | None = None
    today: bool = False
    detail_path: str = Field(min_length=1, max_length=255, validation_alias="detailPath")
    published_on: date | None = Field(default=None, validation_alias="publishedOn")
    visible: bool = True


class AlgorithmUpdate(BaseModel):
    """PATCH body — 보낸 필드만 반영 (exclude_unset). NOT NULL 에 null 은 service 가 422."""

    model_config = ConfigDict(populate_by_name=True)

    slug: str | None = Field(default=None, min_length=1, max_length=64)
    title: str | None = Field(default=None, min_length=1, max_length=128)
    difficulty: str | None = Field(default=None, max_length=8)
    summary: str | None = None
    source_platform: str | None = Field(
        default=None, max_length=32, validation_alias="sourcePlatform"
    )
    source_number: int | None = Field(default=None, validation_alias="sourceNumber")
    source_url: str | None = Field(
        default=None, max_length=255, validation_alias="sourceUrl"
    )
    curated_in: list[str] | None = Field(default=None, validation_alias="curatedIn")
    tags: list[str] | None = None
    today: bool | None = None
    detail_path: str | None = Field(
        default=None, max_length=255, validation_alias="detailPath"
    )
    published_on: date | None = Field(default=None, validation_alias="publishedOn")
    visible: bool | None = None
