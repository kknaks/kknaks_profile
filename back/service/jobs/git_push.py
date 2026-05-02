"""git push retry loop — fetch + rebase + commit + push (spec-03 §5).

STUB — 내일 실제 subprocess 호출 + retry 박을 부분.
현재는 dry_run=True로 호출 시 no-op.
"""

from __future__ import annotations

from datetime import date


def commit_and_push_with_retry(
    today: date,
    max_retries: int = 3,
    dry_run: bool = True,
) -> bool:
    """activity.yaml commit + push (3회 retry).

    spec-03 §5 — 인증은 SSH deploy key (git 프로토콜).
    Returns True if pushed (or dry_run); False if all retries failed.
    """
    if dry_run:
        # M4 stub — 실제 push X. 내일 dry_run=False로 호출
        return True

    # TODO: spec-03 §5 구현
    # for attempt in range(1, max_retries + 1):
    #     try:
    #         subprocess.run(["git", "fetch", "origin"], check=True)
    #         subprocess.run(["git", "rebase", "origin/main"], check=True)
    #         ...
    return False
