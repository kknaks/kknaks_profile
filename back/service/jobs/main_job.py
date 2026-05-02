"""daily_activity_job orchestrator — 입력 → LLM → upsert → push → reload (spec-03 §1, §6)."""

from __future__ import annotations

import logging
from datetime import date

import config
from service.jobs.git_push import commit_and_push_with_retry
from service.jobs.inputs import REPO, fetch_github_events, git_log_today, read_daily_narrative
from service.jobs.llm import summarize_activity
from service.jobs.upsert import upsert_activity

logger = logging.getLogger("kknaks-back.scheduler")

GH_USERS = ["kknaks", "kknaksss"]  # ⚠ kknaksss sign-off 미확정 (M1 sign-off)


async def run_daily_activity_job(dry_run_push: bool | None = None) -> dict:
    """매일 23:55 KST 발동 — spec-03 §1.

    Returns 박힌 entry (테스트/디버깅용).
    dry_run_push 미지정 시 config.job_git_push_dry_run() 사용 (M4 stub 단계 기본 True).
    """
    today = date.today()
    narrative = read_daily_narrative(today)
    notes_changes = git_log_today("persona/notes/", today, REPO)
    contents_changes = git_log_today("persona/contents/", today, REPO)

    commits: list[dict] = []
    for user in GH_USERS:
        commits.extend(await fetch_github_events(user, today))

    resp = summarize_activity(today, narrative, notes_changes, contents_changes, commits)
    entry = {
        "date": today.strftime("%Y.%m.%d"),
        "count": resp["count"],
        "kind": resp["kind"],
        "summary": resp["summary"],
    }

    upsert_activity(entry)
    dry_run = config.job_git_push_dry_run() if dry_run_push is None else dry_run_push
    commit_and_push_with_retry(today, dry_run=dry_run)

    # 메모리 reload — circular import 회피
    from main import load_all

    load_all()
    logger.info("daily_activity_job done: %s", entry)
    return entry
