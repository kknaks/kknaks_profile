"""git fetch + rebase + commit + push (3회 retry) — spec-03 §5, spec-06 §5 공유.

`paths` + `message` 일반화 — 잔디 잡 (activity.yaml) + 콘텐츠 enrich 잡 (contents/*.md) 둘 다 사용.
"""

from __future__ import annotations

import logging
import subprocess
import time
from pathlib import Path

from service.jobs.inputs import REPO

logger = logging.getLogger("kknaks-back.git-push")


def commit_and_push_with_retry(
    paths: list[Path | str],
    message: str,
    *,
    max_retries: int = 3,
    dry_run: bool = True,
    repo_root: Path = REPO,
) -> bool:
    """주어진 paths 를 한 commit 으로 묶어 fetch + rebase 후 push.

    Returns:
        True — pushed (or dry_run, or no-op when paths unchanged).
        False — 모든 retry 실패. 호출자는 다음 tick 에 재시도 가능.

    spec-03 §5 / spec-06 §5 공유 함수. 운영에서 dry_run=False 로 호출.
    """
    if dry_run:
        logger.info("dry_run — skip push (paths=%s, message=%r)", paths, message)
        return True

    str_paths = [str(p) for p in paths]

    for attempt in range(1, max_retries + 1):
        try:
            subprocess.run(
                ["git", "fetch", "origin"],
                cwd=repo_root,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "rebase", "origin/main"],
                cwd=repo_root,
                check=True,
                capture_output=True,
            )

            # 변경 없으면 commit skip (idempotent — 같은 entry 재실행)
            diff = subprocess.run(
                ["git", "diff", "--quiet", "--", *str_paths],
                cwd=repo_root,
            )
            if diff.returncode == 0:
                logger.info("no changes for %s — skip commit", str_paths)
                return True

            subprocess.run(
                ["git", "add", "--", *str_paths],
                cwd=repo_root,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=repo_root,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=repo_root,
                check=True,
                capture_output=True,
            )
            logger.info("pushed: %s", message)
            return True

        except subprocess.CalledProcessError as e:
            stderr = (e.stderr or b"").decode("utf-8", errors="replace")[:500]
            if attempt == max_retries:
                logger.error(
                    "git push failed after %d retries: cmd=%s exit=%d stderr=%s",
                    max_retries,
                    e.cmd,
                    e.returncode,
                    stderr,
                )
                return False
            logger.warning(
                "git push attempt %d/%d failed (cmd=%s): %s — retry",
                attempt,
                max_retries,
                e.cmd,
                stderr,
            )
            time.sleep(2 ** attempt)

    return False
