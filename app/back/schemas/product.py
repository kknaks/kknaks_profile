"""product — front ↔ back 계약. 어드민 회사 제품 화면이 읽고 쓴다.

careerTitle · companyName 은 컬럼이 아니라 2단 조인(product → career → company)의
읽기 전용 표시값이다 — 수정은 careerId 로 한다. visible 은 어드민이라 거르지 않고
그대로 내려준다 — 공개 표면이 서면 그쪽이 거른다.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dto.product import ProductDTO


class AdminProductItem(BaseModel):
    id: int
    career_id: int = Field(serialization_alias="careerId")
    career_title: str = Field(serialization_alias="careerTitle")
    company_name: str = Field(serialization_alias="companyName")
    slug: str
    title: str
    summary: str | None = None
    detail_path: str | None = Field(default=None, serialization_alias="detailPath")
    category: str | None = None
    status: str | None = None
    started_on: date | None = Field(default=None, serialization_alias="startedOn")
    stack: list[str] = []
    thumbnail: str | None = None
    links: dict[str, Any] | None = None
    visible: bool
    # 채팅 노출 토글의 현재값(U-7 — product 확장). PATCH 만 있으면 화면이 항상 off 로 보인다.
    chat_exposed: bool = Field(default=False, serialization_alias="chatExposed")

    @classmethod
    def from_dto(cls, dto: ProductDTO) -> AdminProductItem:
        return cls(
            id=dto.id,
            career_id=dto.career_id,
            career_title=dto.career_title,
            company_name=dto.company_name,
            slug=dto.slug,
            title=dto.title,
            summary=dto.summary,
            detail_path=dto.detail_path,
            category=dto.category,
            status=dto.status,
            started_on=dto.started_on,
            stack=dto.stack or [],
            thumbnail=dto.thumbnail,
            links=dto.links,
            visible=dto.visible,
            chat_exposed=dto.chat_exposed,
        )


class AdminProductsResponse(BaseModel):
    items: list[AdminProductItem]


class ProductCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    career_id: int = Field(validation_alias="careerId")
    slug: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=64)
    summary: str | None = None
    detail_path: str | None = Field(
        default=None, max_length=255, validation_alias="detailPath"
    )
    category: str | None = Field(default=None, max_length=32)
    status: str | None = Field(default=None, max_length=16)
    started_on: date | None = Field(default=None, validation_alias="startedOn")
    stack: list[str] | None = None
    thumbnail: str | None = Field(default=None, max_length=255)
    links: dict[str, Any] | None = None
    visible: bool = True


class ProductUpdate(BaseModel):
    """PATCH body — 보낸 필드만 반영 (exclude_unset). NOT NULL 에 null 은 service 가 422."""

    model_config = ConfigDict(populate_by_name=True)

    career_id: int | None = Field(default=None, validation_alias="careerId")
    slug: str | None = Field(default=None, min_length=1, max_length=64)
    title: str | None = Field(default=None, min_length=1, max_length=64)
    summary: str | None = None
    detail_path: str | None = Field(
        default=None, max_length=255, validation_alias="detailPath"
    )
    category: str | None = Field(default=None, max_length=32)
    status: str | None = Field(default=None, max_length=16)
    started_on: date | None = Field(default=None, validation_alias="startedOn")
    stack: list[str] | None = None
    thumbnail: str | None = Field(default=None, max_length=255)
    links: dict[str, Any] | None = None
    visible: bool | None = None
