"""APScheduler 셋업 (spec-03 §1.1)."""

from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from service.jobs.main_job import run_daily_activity_job

scheduler = AsyncIOScheduler()


def init_scheduler() -> AsyncIOScheduler:
    """daily_activity_job을 매일 00:05 KST에 실행하도록 등록 (직전 날 entry 박음 — spec-03 §1.1)."""
    scheduler.add_job(
        run_daily_activity_job,
        CronTrigger(hour=0, minute=5, timezone="Asia/Seoul"),
        id="daily-activity",
        coalesce=True,
        max_instances=1,
        replace_existing=True,
    )
    return scheduler
