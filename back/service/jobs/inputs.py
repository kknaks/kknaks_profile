"""잔디 잡 입력 4개 수집 (spec-03 §2).

실 동작:
- read_daily_narrative — daily/YYYY-MM-DD.md 본문 read
- git_log_today — 로컬 git log (KST TZ 명시)

Stub (내일 외부 모듈로 교체):
- fetch_github_events — GitHub REST Events API (httpx + KST 변환)
"""

from __future__ import annotations

import subprocess
from datetime import date, timedelta
from pathlib import Path

import frontmatter

import config

REPO = Path(__file__).resolve().parent.parent.parent
PERSONA = config.PERSONA_DIR


def read_daily_narrative(today: date) -> str | None:
    """daily/YYYY-MM-DD.md 본문 (frontmatter 제외). 없으면 None."""
    path = PERSONA / "daily" / f"{today.isoformat()}.md"
    if not path.exists():
        return None
    post = frontmatter.load(path)
    return post.content


def git_log_today(rel_path: str, today: date, repo_root: Path = REPO) -> list[dict]:
    """KST 기준 오늘 commit 목록.

    spec-03 §2.2 — `--since`/`--until`에 명시적 +09:00 ISO timestamp.
    Returns: [{"sha": "...", "subject": "..."}, ...]
    """
    since = f"{today.isoformat()}T00:00:00+09:00"
    until = f"{(today + timedelta(days=1)).isoformat()}T00:00:00+09:00"
    result = subprocess.run(
        [
            "git",
            "log",
            "--since",
            since,
            "--until",
            until,
            "--pretty=format:%H%n%s",
            rel_path,
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    out: list[dict] = []
    if result.returncode != 0 or not result.stdout.strip():
        return out
    lines = result.stdout.strip().split("\n")
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            out.append({"sha": lines[i], "subject": lines[i + 1]})
    return out


async def fetch_github_events(user: str, today: date) -> list[dict]:
    """STUB — 내일 spec-03 §2.4 따라 실제 호출 박을 부분.

    Returns 내일 실제 형식: [{"repo": "...", "msg": "..."}, ...]
    """
    # TODO: httpx + GitHub REST API + _to_kst_date helper (spec-03 §2.4)
    # raise NotImplementedError("GH_TOKEN env 셋업 후 spec-03 §2.4 구현")
    return []
