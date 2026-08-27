"""commit 히스토리 — 2층. 어드민 조회 전용.

수정·삭제가 없다 — 커밋은 수집기(케이스 6·7) 소유다. 날짜 기준은 authored_at
의 **KST 날짜**(/about 잔디 파생과 같은 기준). 한 페이지 50행 고정.
"""

from __future__ import annotations

from calendar import monthrange
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from dataclasses import replace

from core.exceptions import ValidationError
from dto.commit import CommitCalendarDTO, CommitPageDTO
from repository.commit_repo import CommitRepository
from repository.daily_repo import DailyRepository

PAGE_SIZE = 50


def _month_range(year: int, month: int) -> tuple[date, date]:
    """그 달의 [1일, 다음 달 1일)."""
    since = date(year, month, 1)
    until = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    return since, until


class CommitService:
    def __init__(
        self, commit_repo: CommitRepository, daily_repo: DailyRepository
    ) -> None:
        self._commit_repo = commit_repo
        self._daily_repo = daily_repo

    async def get_calendar(
        self, session: AsyncSession, year: int, month: int, repo_id: int | None
    ) -> CommitCalendarDTO:
        """월 달력 — total·repos 는 필터 무관(그 달 전체), days 만 repo 필터.

        days 에 하루 요약(daily 표) 상태를 실어 나른다 — 스트립 빨간 점과
        데일리 카드가 달력 한 번으로 그려지게. daily 는 repo 필터 무관(날짜
        단위 요약)이다.
        """
        since, until = _month_range(year, month)
        days = await self._commit_repo.count_days(session, since, until, repo_id)
        repos = await self._commit_repo.count_repos(session, since, until)
        dailies = await self._daily_repo.map_range(session, since, until)
        days = [
            replace(
                d,
                daily_status=("error" if daily.error else "ok"),
                daily_summary=daily.summary,
                daily_error=daily.error,
                daily_at=daily.updated_at,
            )
            if (daily := dailies.get(date(year, month, d.day))) is not None
            else d
            for d in days
        ]
        return CommitCalendarDTO(
            total=sum(r.count for r in repos),  # 커밋은 레포 정확히 하나에 속한다
            days=days,
            repos=repos,
        )

    async def list_commits(
        self,
        session: AsyncSession,
        year: int,
        month: int,
        repo_id: int | None,
        day: int | None,
        page: int,
    ) -> CommitPageDTO:
        since, until = _month_range(year, month)
        on_day: date | None = None
        if day is not None:
            if not 1 <= day <= monthrange(year, month)[1]:
                raise ValidationError(f"{year}-{month:02d} 에 없는 날짜: {day}")
            on_day = date(year, month, day)
        items, total = await self._commit_repo.list_page(
            session,
            since,
            until,
            repo_id,
            on_day,
            limit=PAGE_SIZE,
            offset=(page - 1) * PAGE_SIZE,
        )
        return CommitPageDTO(items=items, total=total, page=page, page_size=PAGE_SIZE)


commit_service = CommitService(CommitRepository(), DailyRepository())
