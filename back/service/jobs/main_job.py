"""daily_activity_job orchestrator — 입력 → LLM → upsert → push → reload (spec-03 §1, §6)."""

from __future__ import annotations

import logging
from datetime import date

from open_kknaks import ClaudeClient, RedisBroker

import config
from service.jobs.git_push import commit_and_push_with_retry
from service.jobs.inputs import (
    REPO,
    extract_tracked_repos,
    fetch_github_events,
    git_log_today,
    read_daily_narrative,
)
from service.jobs.llm import summarize_activity
from service.jobs.upsert import upsert_activity

logger = logging.getLogger("kknaks-back.scheduler")

LLM_NAMESPACE = "kknaks-portfolio"


async def run_daily_activity_job(
    client: ClaudeClient | None = None,
    *,
    dry_run_push: bool | None = None,
) -> dict:
    """매일 23:55 KST 발동 — spec-03 §1.

    client 미지정 시 self-contained broker (content_enrich 와 동일 패턴).
    """
    today = date.today()
    narrative = read_daily_narrative(today)
    notes_changes = git_log_today("persona/notes/", today, REPO)
    contents_changes = git_log_today("persona/contents/", today, REPO)

    # persona/projects 등록한 레포만 추적 (사용자 결정 — projects 파일이 SoT)
    from main import get_data

    tracked_repos = extract_tracked_repos(get_data().get("projects", []))
    if not tracked_repos:
        logger.info("no tracked repos in persona/projects/*.md — commit fetch skip")

    commits: list[dict] = []
    if tracked_repos:
        for acc in config.gh_accounts():
            commits.extend(
                await fetch_github_events(
                    acc["user"],
                    today,
                    acc["token"],
                    author_email=acc.get("email") or None,
                    tracked_repos=tracked_repos,
                )
            )

    own_broker: RedisBroker | None = None
    if client is None:
        own_broker = RedisBroker(url=config.redis_url(), namespace=LLM_NAMESPACE)
        await own_broker.connect()
        client = ClaudeClient(broker=own_broker)
        logger.info("open-kknaks broker connected (self-contained): %s", config.redis_url())

    try:
        resp = await summarize_activity(
            today, narrative, notes_changes, contents_changes, commits, client
        )
    finally:
        if own_broker is not None:
            await own_broker.close()

    entry = {
        "date": today.strftime("%Y.%m.%d"),
        "count": resp["count"],
        "kind": resp["kind"],
        "summary": resp["summary"],
    }

    upsert_activity(entry)
    dry_run = config.job_git_push_dry_run() if dry_run_push is None else dry_run_push
    commit_and_push_with_retry(
        paths=[config.PERSONA_DIR / "activity.yaml"],
        message=f"chore: activity {today.isoformat()}",
        dry_run=dry_run,
    )

    # 메모리 reload — circular import 회피 (spec-03 §6)
    from main import load_all

    load_all()
    logger.info("daily_activity_job done: %s", entry)
    return entry
