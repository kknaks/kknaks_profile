"""career — front ↔ back 계약. 어드민 역할 화면이 읽고 쓴다.

isCurrent · period 는 컬럼이 아니라 파생값이다(erd.md §career). **여기서만 계산한다** —
프론트는 재계산하지 않는다(lib/types.ts 규약: 두 곳에서 계산하면 형식이 갈린다).
"""

from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dto.career import CareerDTO, PublicCareerBundle
from dto.education import EducationDTO
from dto.problem import ProblemDTO
from dto.product import ProductDTO


def _period(started_on: date, ended_on: date | None) -> str:
    """`2026.02 — 현재` / `2025.08 — 2026.02` — 어드민 회사 화면과 같은 형식."""
    until = "현재" if ended_on is None else f"{ended_on:%Y.%m}"
    return f"{started_on:%Y.%m} — {until}"


class AdminCareerItem(BaseModel):
    id: int
    company_id: int = Field(serialization_alias="companyId")
    company_name: str = Field(serialization_alias="companyName")
    title: str
    started_on: date = Field(serialization_alias="startedOn")
    ended_on: date | None = Field(default=None, serialization_alias="endedOn")
    is_current: bool = Field(serialization_alias="isCurrent")   # ended_on IS NULL
    period: str                                                 # 두 날짜의 렌더
    summary: str | None = None
    description: str | None = None
    stack: list[str] = []
    # 채팅 노출 토글의 현재값(SPEC-017 U-7). PATCH 만 있으면 화면이 항상 off 로 보인다.
    chat_exposed: bool = Field(default=False, serialization_alias="chatExposed")

    @classmethod
    def from_dto(cls, dto: CareerDTO) -> AdminCareerItem:
        return cls(
            id=dto.id,
            company_id=dto.company_id,
            company_name=dto.company_name,
            title=dto.title,
            started_on=dto.started_on,
            ended_on=dto.ended_on,
            is_current=dto.ended_on is None,
            period=_period(dto.started_on, dto.ended_on),
            summary=dto.summary,
            description=dto.description,
            stack=dto.stack or [],
            chat_exposed=dto.chat_exposed,
        )


class AdminCareersResponse(BaseModel):
    items: list[AdminCareerItem]


class CareerCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    company_id: int = Field(validation_alias="companyId")
    title: str = Field(min_length=1, max_length=64)
    started_on: date = Field(validation_alias="startedOn")
    ended_on: date | None = Field(default=None, validation_alias="endedOn")
    summary: str | None = None
    description: str | None = None
    stack: list[str] | None = None


# ── 공개 /api/career — lib/types.ts 의 CareerResponse 와 1:1 ────────────────
#
# 타임라인은 career 와 education 을 합쳐 startedOn DESC 로 그린다(합치는 건 프론트).
# 역할 펼침 = description + 회사 소개 + product 카드 + problem 목록(erd.md §career).
# visible=false 제품은 service 가 걸렀다 — 응답에 visible 필드는 없다(erd §미결 3).


class CareerProductOut(BaseModel):
    """펼침 안의 「만든 것」 카드 한 장."""

    id: int
    slug: str
    title: str
    summary: str | None = None
    category: str | None = None
    status: str | None = None
    started_on: date | None = Field(default=None, serialization_alias="startedOn")
    stack: list[str] = []
    thumbnail: str | None = None
    links: dict[str, Any] | None = None
    body: str | None = None  # detail_path(showcase.md) 전문 — 클릭 모달이 그린다. 끊기면 None

    @classmethod
    def from_dto(cls, dto: ProductDTO, body: str | None = None) -> CareerProductOut:
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
            body=body,
        )


class CareerProblemOut(BaseModel):
    """펼침 안의 「해결한 문제」 한 줄 — 이력서의 알맹이."""

    id: int
    title: str
    body: str | None = None
    product_title: str | None = Field(default=None, serialization_alias="productTitle")

    @classmethod
    def from_dto(cls, dto: ProblemDTO) -> CareerProblemOut:
        return cls(
            id=dto.id, title=dto.title, body=dto.body, product_title=dto.product_title
        )


class PublicCareerItem(BaseModel):
    id: int
    org: str                                                    # company.name
    title: str
    location: str | None = None                                 # company.location — career 엔 컬럼이 없다
    started_on: date = Field(serialization_alias="startedOn")
    ended_on: date | None = Field(default=None, serialization_alias="endedOn")
    is_current: bool = Field(serialization_alias="isCurrent")
    period: str
    summary: str | None = None
    body: str | None = None                                     # career.description — md 원장 없음(erd)
    org_description: str | None = Field(
        default=None, serialization_alias="orgDescription"      # company.description
    )
    stack: list[str] = []
    products: list[CareerProductOut] = []
    problems: list[CareerProblemOut] = []

    @classmethod
    def from_dto(
        cls,
        dto: CareerDTO,
        products: list[ProductDTO],
        problems: list[ProblemDTO],
        product_bodies: dict[int, str] | None = None,
    ) -> PublicCareerItem:
        bodies = product_bodies or {}
        return cls(
            id=dto.id,
            org=dto.company_name,
            title=dto.title,
            location=dto.company_location,
            started_on=dto.started_on,
            ended_on=dto.ended_on,
            is_current=dto.ended_on is None,
            period=_period(dto.started_on, dto.ended_on),
            summary=dto.summary,
            body=dto.description,
            org_description=dto.company_description,
            stack=dto.stack or [],
            products=[CareerProductOut.from_dto(p, bodies.get(p.id)) for p in products],
            problems=[CareerProblemOut.from_dto(p) for p in problems],
        )


class PublicEducationItem(BaseModel):
    id: int
    org: str
    title: str
    location: str | None = None
    started_on: date = Field(serialization_alias="startedOn")
    ended_on: date | None = Field(default=None, serialization_alias="endedOn")
    is_current: bool = Field(serialization_alias="isCurrent")
    period: str
    summary: str | None = None
    body: str | None = None                                     # detail_path md 전문
    stack: list[str] = []

    @classmethod
    def from_dto(cls, dto: EducationDTO, body: str | None) -> PublicEducationItem:
        return cls(
            id=dto.id,
            org=dto.org,
            title=dto.title,
            location=dto.location,
            started_on=dto.started_on,
            ended_on=dto.ended_on,
            is_current=dto.ended_on is None,
            period=_period(dto.started_on, dto.ended_on),
            summary=dto.summary,
            body=body,
            stack=dto.stack or [],
        )


class PublicCareerMeta(BaseModel):
    """좌측 레일 집계 — erd 에 대응 컬럼 없음. 연차·focus 는 profile 에서 왔다."""

    total_roles: str = Field(serialization_alias="totalRoles")
    total_years: str | None = Field(default=None, serialization_alias="totalYears")
    focus: str | None = None


class PublicCareerResponse(BaseModel):
    careers: list[PublicCareerItem] = Field(serialization_alias="career[]")
    education: list[PublicEducationItem] = Field(serialization_alias="education[]")
    career: PublicCareerMeta

    @classmethod
    def from_bundle(cls, bundle: PublicCareerBundle) -> PublicCareerResponse:
        n = len(bundle.careers)
        return cls(
            careers=[
                PublicCareerItem.from_dto(
                    c,
                    bundle.products_by_career.get(c.id, []),
                    bundle.problems_by_career.get(c.id, []),
                    bundle.product_bodies,
                )
                for c in bundle.careers
            ],
            education=[
                PublicEducationItem.from_dto(e, bundle.education_bodies.get(e.id))
                for e in bundle.education
            ],
            career=PublicCareerMeta(
                total_roles=f"{n} role{'s' if n != 1 else ''}",
                total_years=bundle.total_years,
                focus=bundle.focus,
            ),
        )


class CareerUpdate(BaseModel):
    """PATCH body — 보낸 필드만 반영 (exclude_unset). NOT NULL 에 null 은 service 가 422."""

    model_config = ConfigDict(populate_by_name=True)

    company_id: int | None = Field(default=None, validation_alias="companyId")
    title: str | None = Field(default=None, min_length=1, max_length=64)
    started_on: date | None = Field(default=None, validation_alias="startedOn")
    ended_on: date | None = Field(default=None, validation_alias="endedOn")
    summary: str | None = None
    description: str | None = None
    stack: list[str] | None = None
