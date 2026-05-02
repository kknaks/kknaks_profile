"""잔디 잡 입력 4개 수집 (spec-03 §2)."""

from __future__ import annotations

import logging
import subprocess
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import frontmatter
import httpx

import config

logger = logging.getLogger("kknaks-back.inputs")

REPO = Path(__file__).resolve().parent.parent.parent
PERSONA = config.PERSONA_DIR
KST = timezone(timedelta(hours=9))


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


def _to_kst_date(iso_utc: str) -> str:
    """GitHub created_at(UTC, ...Z) → KST 날짜 (YYYY-MM-DD)."""
    return (
        datetime.fromisoformat(iso_utc.replace("Z", "+00:00"))
        .astimezone(KST)
        .date()
        .isoformat()
    )


def extract_tracked_repos(projects: list[dict]) -> set[str]:
    """persona/projects/*.md 의 links.repo 에서 'owner/name' slug 추출.

    `links.repo` 형식: `github.com/owner/name` 또는 `https://github.com/owner/name`.
    GitHub Events API 의 `repo.name` (= 'owner/name') 과 매칭용.
    """
    slugs: set[str] = set()
    for proj in projects or []:
        repo_url = (proj.get("links") or {}).get("repo", "") or ""
        if "github.com/" not in repo_url:
            continue
        slug = repo_url.split("github.com/", 1)[1].rstrip("/").rstrip(".git")
        if slug.count("/") == 1:  # owner/name 형식만
            slugs.add(slug)
    return slugs


async def fetch_github_events(
    user: str,
    today: date,
    token: str,
    author_email: str | None = None,
    tracked_repos: set[str] | None = None,
) -> list[dict]:
    """GitHub REST Events API → 오늘 (KST) PushEvent commits (spec-03 §2.4).

    필터:
    - author_email 박혀있으면 commit author.email 매칭 (본인 commit 만)
    - tracked_repos 박혀있으면 그 repo slug 만 (persona/projects 등록한 레포)
    빈 user/token 이면 skip.

    Returns: [{"repo": "...", "msg": "..."}, ...]
    """
    if not user or not token:
        return []

    today_iso = today.isoformat()
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(
                f"https://api.github.com/users/{user}/events",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github+json",
                },
            )
            r.raise_for_status()
            events = r.json()
    except httpx.HTTPError as e:
        logger.warning("GitHub events fetch failed for %s: %s", user, e)
        return []

    result: list[dict] = []
    for e in events:
        if e.get("type") != "PushEvent":
            continue
        if _to_kst_date(e["created_at"]) != today_iso:
            continue
        repo_slug = e["repo"]["name"]
        if tracked_repos is not None and repo_slug not in tracked_repos:
            continue
        for commit in e.get("payload", {}).get("commits", []):
            # distinct=False 는 이미 다른 push 에 들어간 commit (rebase/cherry-pick 중복) — 제외
            if not commit.get("distinct", True):
                continue
            # author email 매칭 — 박혀있을 때만
            if author_email:
                commit_email = (commit.get("author") or {}).get("email", "")
                if commit_email != author_email:
                    continue
            result.append({"repo": repo_slug, "msg": commit.get("message", "")})
    return result
