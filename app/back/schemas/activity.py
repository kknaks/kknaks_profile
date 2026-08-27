"""activity — front ↔ back 계약. lib/types.ts 의 ActivityResponse 와 1:1 이다.

날짜는 `YYYY.MM.DD` 점 구분이다 — ContribGrass 가 `fmtDateDot` 으로 만든 키와
문자열 비교하므로 다른 형식이면 잔디가 전부 빈 칸이 된다.

counts 는 지금 `commit` 하나만 담는다 — note·study 를 셀 원천이 스키마에 없다
(erd.md §미결 2). 원천이 생기면 키만 늘린다.
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

from dto.activity import ActivityDTO


def _dot(d: date) -> str:
    return d.strftime("%Y.%m.%d")


class ActivityEntryOut(BaseModel):
    date: str
    count: int
    counts: dict[str, int]
    summary: list[str] | None


class ActivityMetaOut(BaseModel):
    total_count: int = Field(serialization_alias="totalCount")
    since: str
    until: str


class ActivityResponse(BaseModel):
    entries: list[ActivityEntryOut] = Field(serialization_alias="activity[]")
    activity: ActivityMetaOut

    @classmethod
    def from_dto(cls, dto: ActivityDTO) -> ActivityResponse:
        return cls(
            entries=[
                ActivityEntryOut(
                    date=_dot(d.day),
                    count=d.count,
                    counts={"commit": d.count},
                    summary=d.summaries or None,
                )
                for d in dto.days
            ],
            activity=ActivityMetaOut(
                total_count=dto.total_count,
                since=_dot(dto.since),
                until=_dot(dto.until),
            ),
        )
