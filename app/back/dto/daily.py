"""daily DTO — 내부 계층 이동용.

하루 요약(daily 표)과, 요약 입력이 되는 그날 커밋 한 건의 최소 모양.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class DailyDTO:
    date: date
    summary: str | None                 # 불릿 — 줄바꿈 구분
    error: str | None                   # 실패 사유. 성공하면 None
    updated_at: datetime


@dataclass(frozen=True)
class DailyCommitDTO:
    """요약 프롬프트에 들어가는 커밋 하나 — message 원문은 AI 입력까지만 간다."""

    id: int
    repo_slug: str                      # owner/name
    is_company: bool                    # 회사 레포 — 프롬프트가 사내 정보를 추상화한다
    message: str | None
