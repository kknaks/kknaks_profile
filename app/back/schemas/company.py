"""company — front ↔ back 계약. 어드민 회사 화면이 읽고 쓴다."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from dto.company import CompanyDTO, CompanyStatsDTO


class CompanyOut(BaseModel):
    id: int
    slug: str
    name: str
    description: str | None = None
    location: str | None = None
    site: str | None = None
    logo_url: str | None = Field(default=None, serialization_alias="logoUrl")
    github_org: str | None = Field(default=None, serialization_alias="githubOrg")

    @classmethod
    def from_dto(cls, dto: CompanyDTO) -> CompanyOut:
        return cls(
            id=dto.id,
            slug=dto.slug,
            name=dto.name,
            description=dto.description,
            location=dto.location,
            site=dto.site,
            logo_url=dto.logo_url,
            github_org=dto.github_org,
        )


class AdminCompanyItem(CompanyOut):
    """회사 + career 파생값 — 이 화면에선 읽기 전용 표시다."""

    career_count: int = Field(serialization_alias="careerCount")
    period: str | None = None    # "2026.02 — 현재". 역할이 없으면 None

    @classmethod
    def from_stats(cls, stats: CompanyStatsDTO) -> AdminCompanyItem:
        period = None
        if stats.started_on is not None:
            until = "현재" if stats.is_current else (
                f"{stats.ended_on:%Y.%m}" if stats.ended_on else "현재"
            )
            period = f"{stats.started_on:%Y.%m} — {until}"
        return cls(
            **CompanyOut.from_dto(stats.company).model_dump(),
            career_count=stats.career_count,
            period=period,
        )


class AdminCompaniesResponse(BaseModel):
    items: list[AdminCompanyItem]


class CompanyCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    slug: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=64)
    description: str | None = None
    location: str | None = None
    site: str | None = None
    logo_url: str | None = Field(default=None, validation_alias="logoUrl")
    github_org: str | None = Field(
        default=None, max_length=64, validation_alias="githubOrg"
    )


class CompanyUpdate(BaseModel):
    """PATCH body — 보낸 필드만 반영 (exclude_unset)."""

    model_config = ConfigDict(populate_by_name=True)

    slug: str | None = Field(default=None, min_length=1, max_length=64)
    name: str | None = Field(default=None, min_length=1, max_length=64)
    description: str | None = None
    location: str | None = None
    site: str | None = None
    logo_url: str | None = Field(default=None, validation_alias="logoUrl")
    github_org: str | None = Field(
        default=None, max_length=64, validation_alias="githubOrg"
    )
