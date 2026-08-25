"""commit — front ↔ back 계약. 어드민 커밋 히스토리(/admin/commits)가 읽는다.

조회 전용 — 입력 스키마가 없다(커밋은 수집기 소유). message 원문은 **어드민
전용**이다 — 공개 표면(/api/activity 등)에는 어떤 형태로도 내리지 않는다.
authoredAt 은 KST 로 변환한 ISO 문자열 — 스트립의 날짜 묶음(KST)과 같은 기준.
"""

from __future__ import annotations

from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field

from dto.commit import CommitCalendarDTO, CommitItemDTO, CommitPageDTO

_KST = ZoneInfo("Asia/Seoul")


class CommitCalendarDayOut(BaseModel):
    day: int                            # 그 달의 일(1~31)
    count: int
    # 하루 요약(daily 표) — 빨간 점·데일리 카드용. dailyStatus null = 행 없음
    daily_status: str | None = Field(None, serialization_alias="dailyStatus")   # "ok" | "error" | null
    daily_summary: list[str] | None = Field(None, serialization_alias="dailySummary")  # 불릿 배열
    daily_error: str | None = Field(None, serialization_alias="dailyError")
    daily_at: str | None = Field(None, serialization_alias="dailyAt")           # KST ISO — 요약/실패 시각


class CommitCalendarRepoOut(BaseModel):
    id: int                             # repo.id — repo_id 필터에 그대로 쓴다
    slug: str                           # owner/name
    count: int


class AdminCommitCalendarResponse(BaseModel):
    total: int                          # 그 달 전체 건수 — repo 필터 무관
    days: list[CommitCalendarDayOut]    # repo 필터 적용
    repos: list[CommitCalendarRepoOut]  # 그 달에 커밋이 있는 레포만 — 필터 무관

    @classmethod
    def from_dto(cls, dto: CommitCalendarDTO) -> AdminCommitCalendarResponse:
        return cls(
            total=dto.total,
            days=[
                CommitCalendarDayOut(
                    day=d.day,
                    count=d.count,
                    daily_status=d.daily_status,
                    daily_summary=(
                        [ln for ln in d.daily_summary.splitlines() if ln.strip()]
                        if d.daily_summary
                        else None
                    ),
                    daily_error=d.daily_error,
                    daily_at=(
                        d.daily_at.astimezone(_KST).isoformat() if d.daily_at else None
                    ),
                )
                for d in dto.days
            ],
            repos=[
                CommitCalendarRepoOut(id=r.id, slug=r.slug, count=r.count)
                for r in dto.repos
            ],
        )


class AdminCommitItem(BaseModel):
    id: int
    repo_slug: str = Field(serialization_alias="repoSlug")   # owner/name
    author: str | None = None
    authored_at: str = Field(serialization_alias="authoredAt")  # KST ISO 문자열
    summary: str | None = None
    message: str | None = None          # 원문 전문 — 어드민 펼침 전용
    sha: str

    @classmethod
    def from_dto(cls, dto: CommitItemDTO) -> AdminCommitItem:
        return cls(
            id=dto.id,
            repo_slug=dto.repo_slug,
            author=dto.author,
            authored_at=dto.authored_at.astimezone(_KST).isoformat(),
            summary=dto.summary,
            message=dto.message,
            sha=dto.sha,
        )


class AdminCommitsResponse(BaseModel):
    items: list[AdminCommitItem]
    total: int                          # 필터(달·레포·날짜) 안의 전체 건수
    page: int
    page_size: int = Field(serialization_alias="pageSize")

    @classmethod
    def from_dto(cls, dto: CommitPageDTO) -> AdminCommitsResponse:
        return cls(
            items=[AdminCommitItem.from_dto(i) for i in dto.items],
            total=dto.total,
            page=dto.page,
            page_size=dto.page_size,
        )
