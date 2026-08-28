"""project — front ↔ back 계약. 어드민 개인 프로젝트 화면 + 공개 /projects.

profile_id 는 계약에 없다 — 1인 사이트라 서버가 첫 profile 로 채운다.
visible 은 어드민만 그대로 내려준다 — 공개 응답은 service 가 걸러서 필드 자체가 없다.
"""

from __future__ import annotations

from collections import Counter
from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dto.project import ProjectDTO, PublicProject


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
    # 채팅 노출 토글의 현재값(SPEC-017 U-7) — `visible` 과 다른 축이다.
    chat_exposed: bool = Field(default=False, serialization_alias="chatExposed")

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
            chat_exposed=dto.chat_exposed,
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


# ── 공개 /api/projects — lib/types.ts 의 ProjectsResponse 와 1:1 ─────────────
#
# visible=false 는 service 가 걸렀다 — 응답에 visible 필드는 없다(erd §미결 3).
# body 는 detail_path md 전문 — 상세 페이지가 별도 API 없이 이걸 쓴다.
# subtitle 은 내리지 않는다 — erd 에 대응 컬럼이 없고 프론트 기본 문구를 쓴다.


class PublicProjectItem(BaseModel):
    id: int
    slug: str
    title: str
    summary: str | None = None
    category: str | None = None
    status: str | None = None
    started_on: date | None = Field(default=None, serialization_alias="startedOn")
    stack: list[str] = []
    thumbnail: str | None = None
    links: dict[str, Any] | None = None                         # {repo, site, store}
    body: str | None = None                                     # detail_path md 전문

    @classmethod
    def from_dto(cls, item: PublicProject) -> PublicProjectItem:
        dto = item.dto
        return cls(
            id=dto.id,
            slug=dto.slug,
            title=dto.title,
            summary=dto.summary,
            category=dto.category,
            status=dto.status,
            started_on=dto.started_on,
            stack=dto.stack or [],
            thumbnail=dto.thumbnail,
            links=dto.links,
            body=item.body,
        )


class PublicProjectCategory(BaseModel):
    """`GROUP BY category` 의 파생(database.md §product) — id·label 은 category 그대로."""

    id: str
    label: str
    count: int


class PublicProjectsMeta(BaseModel):
    total_count: int = Field(serialization_alias="totalCount")
    categories: list[PublicProjectCategory] = []


class PublicProjectsResponse(BaseModel):
    items: list[PublicProjectItem] = Field(serialization_alias="projects[]")
    projects: PublicProjectsMeta

    @classmethod
    def from_public(cls, projects: list[PublicProject]) -> PublicProjectsResponse:
        # category 가 NULL 인 항목은 목록엔 뜨되 집계에서 빠진다 — count 내림차순.
        counts = Counter(
            p.dto.category for p in projects if p.dto.category is not None
        )
        return cls(
            items=[PublicProjectItem.from_dto(p) for p in projects],
            projects=PublicProjectsMeta(
                total_count=len(projects),
                categories=[
                    PublicProjectCategory(id=c, label=c, count=n)
                    for c, n in counts.most_common()
                ],
            ),
        )
