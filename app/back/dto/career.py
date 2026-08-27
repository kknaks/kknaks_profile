"""역할(career) DTO — 내부 계층 이동용."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dto.education import EducationDTO
    from dto.problem import ProblemDTO
    from dto.product import ProductDTO


@dataclass(frozen=True)
class CareerDTO:
    """career 행 + 회사 이름. is_current · period 는 여기 없다 — 표현은 schemas 가 한다."""

    id: int
    profile_id: int
    company_id: int
    company_name: str
    title: str
    started_on: date
    ended_on: date | None
    summary: str | None
    description: str | None
    stack: list[str] | None

    # 역할별 persona md(DB 파생물)의 위치. 비어 있으면 렌더가 경로를 파생한다.
    persona_path: str | None = None

    # 공개 /career 가 쓰는 회사 속성 — career 에는 location 컬럼이 없어 회사 것을
    # 쓰고, 펼침의 회사 소개도 여기서 온다(erd.md §career). 어드민 경로는 안 채운다.
    company_location: str | None = None
    company_description: str | None = None


@dataclass(frozen=True)
class PublicCareerBundle:
    """공개 /career 한 벌 — 타임라인이 한 번에 그릴 것 전부.

    총연차·focus 는 profile 에서 온다 — 같은 사실을 두 곳에 두지 않는다.
    """

    careers: list[CareerDTO]
    products_by_career: dict[int, list[ProductDTO]] = field(default_factory=dict)
    product_bodies: dict[int, str] = field(default_factory=dict)     # product id → detail_path md 전문
    problems_by_career: dict[int, list[ProblemDTO]] = field(default_factory=dict)
    education: list[EducationDTO] = field(default_factory=list)
    education_bodies: dict[int, str] = field(default_factory=dict)  # id → detail_path md 전문
    total_years: str | None = None                                  # profile.years
    focus: str | None = None                                        # profile.focus
