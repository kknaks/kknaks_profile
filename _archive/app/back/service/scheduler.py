"""APScheduler 셋업 — daily-activity (잔디) + neetcode-canonical (algorithm) 두 잡."""

from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from service.jobs.algorithms.main import run_neetcode_canonical_job
from service.pipeline.daily_intake import run_daily_intake_job

scheduler = AsyncIOScheduler()


def init_scheduler() -> AsyncIOScheduler:
    """두 잡 등록.

    - **daily-activity**: 매일 **09:05 KST** = 00:05 UTC. 어제 entry (spec-03 §1.1).
      자정 직후 발동 시 `date.today() - 1d` 가 그저께가 되는 off-by-one 회피.
    - **neetcode-canonical**: 매일 **23:00 UTC** = KST 다음날 08:00. NeetCode 150 다음 항목 박음 (spec-03 §11, spec-07 §7).

    **잔디 잡은 이제 접수만 한다** (KDEV-WORK-017 P5). 종전 `run_daily_activity_job` 은
    조사·요약·파일 쓰기·push 를 잡 안에서 다 했다 — 사람의 승인 없이 레포에 쓰이는
    경로였고, 그것을 없애는 것이 이 발주의 목적이다. 조사와 작성과 발행은 드라이버와
    게이트가 이어받는다.
    """
    # 잔디 잡 — 접수 한 건. 조사는 드라이버가, 발행은 승인이 민다.
    scheduler.add_job(
        run_daily_intake_job,
        CronTrigger(hour=9, minute=5, timezone="Asia/Seoul"),
        id="daily-activity",
        coalesce=True,
        max_instances=1,
        replace_existing=True,
    )
    # algorithm 잡 (별도 큐 — spec-03 §11)
    scheduler.add_job(
        run_neetcode_canonical_job,
        CronTrigger(hour=23, minute=0, timezone="UTC"),
        id="neetcode-canonical",
        coalesce=True,
        max_instances=1,
        replace_existing=True,
    )
    return scheduler
