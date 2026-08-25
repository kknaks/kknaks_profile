"""commit DTO — 내부 계층 이동용.

어드민 커밋 히스토리(/admin/commits) 조회 전용 — 수정·삭제가 없다(커밋은
수집기 소유). 날짜 기준은 authored_at 의 **KST 날짜**다(/about 잔디 파생과
같은 기준).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CommitDayCountDTO:
    day: int                            # 그 달의 일(1~31)
    count: int
    # 하루 요약(daily 표) — 스트립 빨간 점·데일리 카드용. None = 행 없음(미요약)
    daily_status: str | None = None     # "ok" | "error" | None
    daily_summary: str | None = None    # 불릿 원문(줄바꿈 구분)
    daily_error: str | None = None      # 실패 사유
    daily_at: datetime | None = None    # daily.updated_at — 요약/실패 시각


@dataclass(frozen=True)
class CommitRepoCountDTO:
    id: int                             # repo.id
    slug: str                           # owner/name
    count: int                          # 그 달 커밋 수


@dataclass(frozen=True)
class CommitCalendarDTO:
    total: int                          # 그 달 전체 건수 — repo 필터 무관
    days: list[CommitDayCountDTO]       # repo 필터 적용
    repos: list[CommitRepoCountDTO]     # 그 달에 커밋이 있는 레포만 — 필터 무관


@dataclass(frozen=True)
class CommitItemDTO:
    id: int
    repo_slug: str                      # owner/name — 표시는 name 부분
    author: str | None
    authored_at: datetime               # timestamptz — 표현(KST)은 schemas 가 한다
    summary: str | None                 # 한 줄 요약. 잔디에 뜨는 값
    message: str | None                 # 원문 — 어드민 전용. 공개 표면 금지
    sha: str


@dataclass(frozen=True)
class CommitPageDTO:
    items: list[CommitItemDTO]
    total: int                          # 필터(달·레포·날짜) 안의 전체 건수
    page: int
    page_size: int
