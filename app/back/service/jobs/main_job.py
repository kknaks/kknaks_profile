"""daily_activity_job orchestrator — inputs → counts (deterministic) + LLM body·summary
→ daily/{date}.md write → push → reload (spec-03 §1·§6, ADR-06)."""

from __future__ import annotations

import logging
from datetime import date, timedelta

from open_kknaks import ClaudeClient, RedisBroker

import config
from service.jobs.git_push import commit_and_push_with_retry
from service.jobs.inputs import (
    REPO,
    extract_tracked_repos,
    fetch_repo_commits,
    read_changed_files_today,
    read_existing_daily,
)
from service.jobs.llm import summarize_daily
from service.jobs.upsert import write_daily
from service.notify import notify_slack

logger = logging.getLogger("kknaks-back.scheduler")

LLM_NAMESPACE = "kknaks-portfolio"


async def run_daily_activity_job(
    client: ClaudeClient | None = None,
    *,
    dry_run_push: bool | None = None,
    target_date: date | None = None,
) -> dict:
    """매일 09:05 KST 발동 — 직전 날 daily/{date}.md 자동 작성 (spec-03 §1, ADR-06).

    client 미지정 시 self-contained broker (content_enrich 와 동일 패턴).
    target_date 미지정 시 어제 (`date.today() - 1`) — 백필/테스트용 override.
    09:05 KST = 00:05 UTC — 컨테이너 TZ (UTC) 의 `date.today()` 가 어제 KST 와 일치.
    """
    target = target_date if target_date is not None else date.today() - timedelta(days=1)
    target_iso = target.isoformat()

    # spec-03 §1.3 — 본인 작성 (auto:false 또는 미박음) 우선. 잡 skip.
    existing = read_existing_daily(target)
    if existing and not existing.get("auto"):
        logger.info(
            "daily/%s.md 본인 작성 (auto=%r) — 잡 skip",
            target_iso,
            existing.get("auto"),
        )
        await notify_slack(f":raised_hand: 잔디 잡 skip — daily/{target_iso}.md 본인 작성")
        return {
            "date": target.strftime("%Y.%m.%d"),
            "skipped": True,
            "reason": "user_authored",
        }

    try:
        return await _do_run_daily_activity_job(target, client, dry_run_push)
    except Exception as e:
        logger.exception("daily_activity_job failed for target=%s", target_iso)
        await notify_slack(
            f":x: 잔디 잡 실패 — daily/{target_iso}\n"
            f"`{type(e).__name__}: {str(e)[:300]}`"
        )
        raise


async def _do_run_daily_activity_job(
    target: date,
    client: ClaudeClient | None,
    dry_run_push: bool | None,
) -> dict:
    """잡 본체 — 호출자 (run_daily_activity_job) 가 try/except 로 감쌈."""
    notes_changes = read_changed_files_today("reference/", target, REPO)
    contents_changes = read_changed_files_today("persona/contents/", target, REPO, max_chars_per_file=2048)

    # products/*/showcase.md 등록한 레포만 추적 (사용자 결정 — showcase 파일이 SoT)
    from main import get_data

    tracked_repos = extract_tracked_repos(get_data().get("projects", []))
    if not tracked_repos:
        logger.info("no tracked repos in products/*/showcase.md — commit fetch skip")

    # 각 tracked repo × 각 acc 조합 호출 + (repo, msg) 키 dedupe
    seen: set[tuple[str, str]] = set()
    commits: list[dict] = []
    accounts = config.gh_accounts()
    for repo in tracked_repos:
        for acc in accounts:
            fetched = await fetch_repo_commits(
                repo,
                target,
                acc["token"],
                author=acc["user"],
            )
            for c in fetched:
                key = (c["repo"], c["msg"])
                if key in seen:
                    continue
                seen.add(key)
                commits.append(c)

    # spec-03 §3.1 — counts 코드 계산 (LLM 안 거침)
    counts = {
        "commit": len(commits),
        "note": len(notes_changes),
        "study": len(contents_changes),
    }

    own_broker: RedisBroker | None = None
    if client is None:
        own_broker = RedisBroker(url=config.redis_url(), namespace=LLM_NAMESPACE)
        await own_broker.connect()
        client = ClaudeClient(broker=own_broker)
        logger.info("open-kknaks broker connected (self-contained): %s", config.redis_url())

    try:
        resp = await summarize_daily(
            target, notes_changes, contents_changes, commits, counts, client
        )
    finally:
        if own_broker is not None:
            await own_broker.close()

    path = write_daily(target, counts, resp.get("summary"), resp.get("body", ""))

    dry_run = config.job_git_push_dry_run() if dry_run_push is None else dry_run_push
    commit_and_push_with_retry(
        paths=[path],
        message=f"chore: daily {target.isoformat()}",
        dry_run=dry_run,
    )

    # 메모리 reload — circular import 회피 (spec-03 §6). KDEV-WORK-007 — enforce 실패 시
    # reload_data 가 구 데이터 유지·False 반환(워커 크래시 금지). 잡은 이미 commit/push 완료.
    from main import reload_data

    reload_data()
    entry = {
        "date": target.strftime("%Y.%m.%d"),
        "counts": counts,
        "summary": resp.get("summary"),
    }
    logger.info("daily_activity_job done: %s", entry)

    summary_ko = (resp.get("summary") or {}).get("ko") or "(활동 없음)"
    push_status = "dry-run" if dry_run else "pushed"
    await notify_slack(
        f":seedling: 잔디 잡 — daily/{target.isoformat()} ({push_status})\n"
        f"counts: commit={counts['commit']} note={counts['note']} study={counts['study']}\n"
        f"{summary_ko}"
    )

    return entry
