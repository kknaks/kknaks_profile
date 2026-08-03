"""레포 작업트리에서 읽는 잔디 입력 (spec-03 §2 잔여).

**커밋 조사는 여기 없다.** GitHub API 로 커밋을 긁던 `fetch_repo_commits`·
`extract_tracked_repos`·`git_log_today` 는 KDEV-WORK-017 P5 에서 걷혔다 — 이제
조사는 서버의 bare 클론을 읽는 `service/jobs/collect_commits.py` 가 한다.

남은 것은 **프로필 레포 자신의 변경**을 읽는 함수들이다. 그건 bare 클론이 아니라
작업트리에 있고, `counts` 의 `note`·`study` 가 여기서 나온다.
"""

from __future__ import annotations

import logging
import subprocess
from datetime import date, timedelta
from pathlib import Path

import frontmatter

import config

logger = logging.getLogger("kknaks-back.inputs")

REPO = Path(__file__).resolve().parents[4]
PERSONA = config.PERSONA_DIR


def read_daily_narrative(today: date) -> str | None:
    """daily/YYYY-MM-DD.md 본문 (frontmatter 제외). 없으면 None.

    spec-03 이전 spec 의 1순위 narrative 입력. 새 flow (ADR-06) 에선 §1.3 본인작성 검사용.
    """
    path = PERSONA / "daily" / f"{today.isoformat()}.md"
    if not path.exists():
        return None
    post = frontmatter.load(path)
    return post.content


def read_existing_daily(target: date) -> dict | None:
    """daily/YYYY-MM-DD.md frontmatter 읽기. 없으면 None.

    spec-03 §1.3 — 본인 작성 (`auto: false` 또는 미박음) 시 잡 skip 판단용.
    """
    path = PERSONA / "daily" / f"{target.isoformat()}.md"
    if not path.exists():
        return None
    post = frontmatter.load(path)
    return dict(post.metadata)


def read_changed_files_today(
    rel_path: str,
    target: date,
    repo_root: Path = REPO,
    *,
    max_chars_per_file: int = 4096,
) -> list[dict]:
    """target 날 (KST) 에 변경된 .md 파일들의 frontmatter + 본문.

    spec-03 §2.1·§2.2 — git log --name-only 로 그날 변경 파일 추출 후
    각 파일의 본문 (frontmatter 제외) 을 읽어 LLM 컨텍스트로 사용.

    Returns: [{"path", "frontmatter", "body"}, ...]. 본문은 max_chars_per_file 자 truncate.
    """
    since = f"{target.isoformat()}T00:00:00+09:00"
    until = f"{(target + timedelta(days=1)).isoformat()}T00:00:00+09:00"
    result = subprocess.run(
        [
            "git",
            "log",
            "--since",
            since,
            "--until",
            until,
            "--name-only",
            "--pretty=format:",
            rel_path,
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []

    paths = sorted({line.strip() for line in result.stdout.splitlines() if line.strip().endswith(".md")})

    out: list[dict] = []
    for p in paths:
        full = repo_root / p
        if not full.exists():
            continue  # commit 후 삭제된 파일
        try:
            post = frontmatter.load(full)
        except Exception as e:  # noqa: BLE001
            logger.warning("frontmatter parse fail for %s: %s — skip", p, e)
            continue
        body = post.content or ""
        if len(body) > max_chars_per_file:
            body = body[:max_chars_per_file] + "\n...(truncated)"
        out.append({"path": p, "frontmatter": dict(post.metadata), "body": body})
    return out





