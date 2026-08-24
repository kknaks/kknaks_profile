"""career — front ↔ back 계약. 어드민 역할 화면이 읽고 쓴다.

isCurrent · period 는 컬럼이 아니라 파생값이다(erd.md §career). **여기서만 계산한다** —
프론트는 재계산하지 않는다(lib/types.ts 규약: 두 곳에서 계산하면 형식이 갈린다).
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from dto.career import CareerDTO


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
