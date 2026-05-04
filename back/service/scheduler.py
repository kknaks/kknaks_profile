"""APScheduler 셋업 (spec-03 §1.1)."""

from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from service.jobs.main_job import run_daily_activity_job

scheduler = AsyncIOScheduler()


def init_scheduler() -> AsyncIOScheduler:
    """daily_activity_job을 매일 09:05 KST에 실행하도록 등록 (직전 날 entry 박음 — spec-03 §1.1).

    09:05 KST = 00:05 UTC — 컨테이너 TZ (UTC) 기준 `date.today() - 1d` 가
    "어제 KST" 와 일치하는 시각. 자정 직후 발동 (00:05 KST = 15:05 UTC 전날) 이면
    `date.today()` 가 그저께를 반환하는 off-by-one 발생 (b6979da 사고 회피).
    """
    scheduler.add_job(
        run_daily_activity_job,
        CronTrigger(hour=9, minute=5, timezone="Asia/Seoul"),
        id="daily-activity",
        coalesce=True,
        max_instances=1,
        replace_existing=True,
    )
    return scheduler
