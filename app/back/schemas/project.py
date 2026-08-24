"""project — front ↔ back 계약. 어드민 개인 프로젝트 화면이 읽고 쓴다.

profile_id 는 계약에 없다 — 1인 사이트라 서버가 첫 profile 로 채운다.
visible 은 어드민이라 거르지 않고 그대로 내려준다 — 공개 표면이 서면 그쪽이 거른다.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dto.project import ProjectDTO


class AdminProjectItem(BaseModel):
    id: int
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

    @classmethod
    def from_dto(cls, dto: ProjectDTO) -> AdminProjectItem:
        return cls(
            id=dto.id,
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
        )


class AdminProjectsResponse(BaseModel):
    items: list[AdminProjectItem]


class ProjectCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

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


class ProjectUpdate(BaseModel):
    """PATCH body — 보낸 필드만 반영 (exclude_unset). NOT NULL 에 null 은 service 가 422."""

    model_config = ConfigDict(populate_by_name=True)

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
