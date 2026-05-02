"""git fetch + rebase + commit + push (3회 retry) — spec-03 §5, spec-06 §5 공유.

`paths` + `message` 일반화 — 잔디 잡 (activity.yaml) + 콘텐츠 enrich 잡 (contents/*.md) 둘 다 사용.

인증/identity (planning-01 §3.6 ③/④):
- token = `config.bot_identity()["token"]` → `http.https://github.com/.extraheader=Authorization: Basic <base64(x-access-token:TOKEN)>`.
  GitHub Actions checkout action 의 canonical 패턴. `bearer` 는 REST API 용이라 git-over-HTTPS 작동 보장 X.
  url-embed (`https://user:token@...`) 회피 — argv/reflog 노출 차단.
- commit author = bot_identity 의 user/email — webhook self-push 필터(`bot_emails()`)와 매칭 필수.
"""

from __future__ import annotations

import base64
import logging
import subprocess
import time
from pathlib import Path

import config
from service.jobs.inputs import REPO

logger = logging.getLogger("kknaks-back.git-push")


def _build_auth_args(token: str) -> list[str]:
    """git -c http.<url>.extraheader=... 형식 — Basic + base64 encoded."""
    basic = base64.b64encode(f"x-access-token:{token}".encode()).decode()
    return ["-c", f"http.https://github.com/.extraheader=Authorization: Basic {basic}"]


def _redact_cmd(cmd) -> list[str]:
    """logger 출력용 — extraheader 의 token 을 가린 cmd."""
    safe: list[str] = []
    for s in cmd or []:
        if isinstance(s, str) and "Authorization:" in s:
            safe.append("-c http.<redacted-extraheader>")
        else:
            safe.append(str(s))
    return safe


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
        False — 모든 retry 실패 또는 bot_identity 미설정. 호출자는 다음 tick 에 재시도 가능.

    spec-03 §5 / spec-06 §5 공유 함수. 운영에서 dry_run=False 로 호출.
    """
    if dry_run:
        logger.info("dry_run — skip push (paths=%s, message=%r)", paths, message)
        return True

    identity = config.bot_identity()
    if identity is None:
        logger.error("bot_identity 미설정 (GH_USER_PERSONAL/GH_TOKEN_PERSONAL/GH_EMAIL_PERSONAL) — push skip")
        return False

    auth = _build_auth_args(identity["token"])
    author = [
        "-c", f"user.email={identity['email']}",
        "-c", f"user.name={identity['user']}",
    ]
    str_paths = [str(p) for p in paths]

    for attempt in range(1, max_retries + 1):
        try:
            subprocess.run(
                ["git", *auth, "fetch", "origin"],
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
                ["git", *author, "commit", "-m", message],
                cwd=repo_root,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", *auth, "push", "origin", "main"],
                cwd=repo_root,
                check=True,
                capture_output=True,
            )
            logger.info("pushed: %s", message)
            return True

        except subprocess.CalledProcessError as e:
            stderr = (e.stderr or b"").decode("utf-8", errors="replace")[:500]
            cmd_safe = _redact_cmd(e.cmd if isinstance(e.cmd, list) else [e.cmd])
            if attempt == max_retries:
                logger.error(
                    "git push failed after %d retries: cmd=%s exit=%d stderr=%s",
                    max_retries,
                    cmd_safe,
                    e.returncode,
                    stderr,
                )
                return False
            logger.warning(
                "git push attempt %d/%d failed (cmd=%s): %s — retry",
                attempt,
                max_retries,
                cmd_safe,
                stderr,
            )
            time.sleep(2 ** attempt)

    return False
