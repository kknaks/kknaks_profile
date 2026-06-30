"""neetcode_canonical_job orchestrator — 5단계 파이프라인 (spec-07 §7.1, spec-03 §11).

매일 23:00 UTC 발동:
1. NeetCode 150 시퀀스 fetch + count_existing → next_index
2. (a) source fetch (LeetCode GraphQL + neetcode-gh)
3. (b) 캐시 (in-process, 잡 1회 안에서만)
4. (c) 정규화 (deterministic — params split·core_lines AST)
5. (d) LLM gap-filler (open-kknaks 1 호출)
6. (e) write md + today mutation
7. commit + push
8. load_all reload
9. slack notify (성공·실패·시퀀스 끝)
"""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path

from open_kknaks import ClaudeClient, RedisBroker

import config
from service.jobs.algorithms.fetch import (
    DictCache,
    fetch_leetcode,
    fetch_neetcode_gh,
)
from service.jobs.algorithms.llm_fillgaps import fill_gaps
from service.jobs.algorithms.normalize import normalize_question
from service.jobs.algorithms.sequence import (
    count_existing_algorithms,
    fetch_neetcode_150,
    get_next,
)
from service.jobs.algorithms.write import (
    clear_today_flag,
    write_algorithm_md,
)
from service.jobs.git_push import commit_and_push_with_retry
from service.notify import notify_slack

logger = logging.getLogger("kknaks-back.scheduler")

LLM_NAMESPACE = "kknaks-portfolio"


async def run_neetcode_canonical_job(
    client: ClaudeClient | None = None,
    *,
    dry_run_push: bool | None = None,
    target_date: date | None = None,
    persona_dir: Path | None = None,
) -> dict:
    """매일 23:00 UTC 발동 — NeetCode 150 다음 항목 박음 (spec-07 §7.1, spec-03 §11).

    `persona/algorithms/A-NNN-slug.md` 1개 + commit/push.

    Args:
        client: open-kknaks ClaudeClient. None 이면 self-contained broker 생성.
        dry_run_push: git push dry-run override.
        target_date: 박는 날 (UTC). 미지정 시 today.
        persona_dir: 미지정 시 config.PERSONA_DIR.
    """
    target = target_date if target_date is not None else date.today()
    persona = persona_dir if persona_dir is not None else config.PERSONA_DIR

    try:
        return await _do_run_neetcode_canonical_job(
            client, dry_run_push, target, persona
        )
    except Exception as e:
        logger.exception(
            "neetcode_canonical_job failed for target=%s", target.isoformat()
        )
        await notify_slack(
            f":x: algorithm 잡 실패 — {target.isoformat()}\n"
            f"`{type(e).__name__}: {str(e)[:300]}`"
        )
        raise


async def _do_run_neetcode_canonical_job(
    client: ClaudeClient | None,
    dry_run_push: bool | None,
    target: date,
    persona: Path,
) -> dict:
    """잡 본체 — 호출자 (run_neetcode_canonical_job) 가 try/except 로 감쌈."""
    cache = DictCache()  # process-local — 같은 잡 1회 내 중복 호출 방어

    # 시퀀스 + 다음 idx
    items = await fetch_neetcode_150(cache=cache)
    idx = count_existing_algorithms(persona)
    seq = get_next(items, idx)

    if seq is None:
        msg = f":checkered_flag: NeetCode 150 시퀀스 완료 (idx={idx} / {len(items)})"
        logger.info(msg)
        await notify_slack(msg)
        return {
            "date": target.isoformat(),
            "skipped": True,
            "reason": "sequence_end",
            "idx": idx,
        }

    a_id = f"A-{idx + 1:03d}"
    logger.info(
        "neetcode_canonical: a_id=%s slug=%s pattern=%s difficulty=%s",
        a_id,
        seq.slug,
        seq.pattern,
        seq.difficulty,
    )

    # (a) raw fetch + (b) cache (함수 내부 캐시)
    q = await fetch_leetcode(seq.slug, cache=cache)
    code = await fetch_neetcode_gh(seq.slug, seq.number, cache=cache)

    # (c) normalize
    normalized = normalize_question(q, code)

    # (d) LLM gap-filler
    own_broker: RedisBroker | None = None
    if client is None:
        own_broker = RedisBroker(url=config.redis_url(), namespace=LLM_NAMESPACE)
        await own_broker.connect()
        client = ClaudeClient(broker=own_broker)
        logger.info(
            "open-kknaks broker connected (self-contained): %s", config.redis_url()
        )

    try:
        llm_result = await fill_gaps(normalized, client=client)
    finally:
        if own_broker is not None:
            await own_broker.close()

    # (e) write md + clear today
    new_path = write_algorithm_md(
        a_id=a_id,
        sequence_item=seq,
        normalized=normalized,
        llm_result=llm_result,
        target_date=target,
        persona_dir=persona,
    )
    cleared = clear_today_flag(persona, except_path=new_path)

    # commit + push
    dry_run = config.job_git_push_dry_run() if dry_run_push is None else dry_run_push
    commit_and_push_with_retry(
        paths=[new_path] + cleared,
        message=f"chore: algorithm {a_id} {seq.slug}",
        dry_run=dry_run,
    )

    # 메모리 reload — circular import 회피 (spec-03 §6). KDEV-WORK-007 — enforce 실패 시
    # reload_data 가 구 데이터 유지·False 반환(워커 크래시 금지). 잡은 이미 commit/push 완료.
    from main import reload_data

    reload_data()

    # slack notify
    n_clarifying = len(llm_result.get("clarifying_items", []))
    n_approach = len(llm_result.get("approach_items", []))
    n_logic = len(llm_result.get("logic_slots", []))
    n_followup = len(llm_result.get("solution", {}).get("followup", []))
    push_status = "dry-run" if dry_run else "pushed"
    await notify_slack(
        f":dna: algorithm 잡 — {a_id} {seq.slug} ({push_status})\n"
        f"pattern: {seq.pattern} · difficulty: {normalized.get('difficulty', '?')}\n"
        f"clarifying {n_clarifying} / approach {n_approach} / logic {n_logic} slots / followup {n_followup}"
    )

    entry = {
        "date": target.isoformat(),
        "a_id": a_id,
        "slug": seq.slug,
        "number": seq.number,
        "pattern": seq.pattern,
        "difficulty": normalized.get("difficulty"),
        "path": str(new_path.relative_to(persona) if new_path.is_absolute() else new_path),
        "cleared_count": len(cleared),
    }
    logger.info("neetcode_canonical_job done: %s", entry)
    return entry
