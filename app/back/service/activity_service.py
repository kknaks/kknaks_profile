"""activity — 2층. 잔디 창은 「지난 1년」이다(화면이 53주 격자를 그린다).

날짜별 문장(summary)은 **daily.summary 의 불릿**만 내린다. daily 행이 없거나
error 상태면 빈 배열 — 커밋 첫 줄 fallback 을 두지 않는다. **이유: 공개
표면이라, 회사 레포 커밋 메시지 원문(사내 정보)이 그대로 노출되면 안 된다.**
추상화를 거친 AI 요약(daily)만이 공개 자격이 있다.
"""

from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from dto.activity import ActivityDayDTO, ActivityDTO
from repository.commit_repo import CommitRepository
from repository.daily_repo import DailyRepository

_WINDOW_DAYS = 365


class ActivityService:
    def __init__(
        self, commit_repo: CommitRepository, daily_repo: DailyRepository
    ) -> None:
        self._commit_repo = commit_repo
        self._daily_repo = daily_repo

    async def get_activity(self, session: AsyncSession) -> ActivityDTO:
        until = date.today()
        since = until - timedelta(days=_WINDOW_DAYS - 1)
        counts = await self._commit_repo.list_daily(session, since)
        dailies = await self._daily_repo.map_range(session, since)
        days = []
        for day, count in counts:
            daily = dailies.get(day)
            # daily 없음 · error → 빈 배열. 커밋 첫 줄로 메우지 않는다(위 docstring).
            summaries = (
                [ln for ln in daily.summary.splitlines() if ln.strip()]
                if daily is not None and daily.error is None and daily.summary
                else []
            )
            days.append(ActivityDayDTO(day=day, count=count, summaries=summaries))
        return ActivityDTO(
            days=days,
            total_count=sum(d.count for d in days),
            since=since,
            until=until,
        )


activity_service = ActivityService(CommitRepository(), DailyRepository())
