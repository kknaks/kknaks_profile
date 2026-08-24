"""education — front ↔ back 계약. 어드민 교육 화면이 읽고 쓴다.

isCurrent · period 는 컬럼이 아니라 파생값이다(erd.md §education 대응 없음 —
career 와 같은 파생 규약). **여기서만 계산한다** — 프론트는 재계산하지 않는다
(lib/types.ts 규약: 두 곳에서 계산하면 형식이 갈린다).
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from dto.education import EducationDTO


def _period(started_on: date, ended_on: date | None) -> str:
    """`2024.12 — 2025.03` / `2026.02 — 현재` — 어드민 역할 화면과 같은 형식."""
    until = "현재" if ended_on is None else f"{ended_on:%Y.%m}"
    return f"{started_on:%Y.%m} — {until}"


class AdminEducationItem(BaseModel):
    id: int
    org: str
    title: str
    location: str | None = None
    started_on: date = Field(serialization_alias="startedOn")
    ended_on: date | None = Field(default=None, serialization_alias="endedOn")
    is_current: bool = Field(serialization_alias="isCurrent")   # ended_on IS NULL
    period: str                                                 # 두 날짜의 렌더
    summary: str | None = None
    detail_path: str | None = Field(default=None, serialization_alias="detailPath")
    stack: list[str] = []

    @classmethod
    def from_dto(cls, dto: EducationDTO) -> AdminEducationItem:
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
            detail_path=dto.detail_path,
            stack=dto.stack or [],
        )


class AdminEducationsResponse(BaseModel):
    items: list[AdminEducationItem]


class EducationCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    org: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=64)
    location: str | None = Field(default=None, max_length=64)
    started_on: date = Field(validation_alias="startedOn")
    ended_on: date | None = Field(default=None, validation_alias="endedOn")
    summary: str | None = None
    detail_path: str | None = Field(
        default=None, max_length=255, validation_alias="detailPath"
    )
    stack: list[str] | None = None


class EducationUpdate(BaseModel):
    """PATCH body — 보낸 필드만 반영 (exclude_unset). NOT NULL 에 null 은 service 가 422."""

    model_config = ConfigDict(populate_by_name=True)

    org: str | None = Field(default=None, min_length=1, max_length=64)
    title: str | None = Field(default=None, min_length=1, max_length=64)
    location: str | None = Field(default=None, max_length=64)
    started_on: date | None = Field(default=None, validation_alias="startedOn")
    ended_on: date | None = Field(default=None, validation_alias="endedOn")
    summary: str | None = None
    detail_path: str | None = Field(
        default=None, max_length=255, validation_alias="detailPath"
    )
    stack: list[str] | None = None
