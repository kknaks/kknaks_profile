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
        # rstrip(".git") 은 문자집합 — 끝글자가 g/i/t 면 의도치 않게 잘림 (e.g. wine_log → wine_lo)
        slug = repo_url.split("github.com/", 1)[1].rstrip("/")
        if slug.endswith(".git"):
            slug = slug[:-4]
        if slug.count("/") == 1:  # owner/name 형식만
            slugs.add(slug)
    return slugs


async def fetch_repo_commits(
    owner_repo: str,
    today: date,
    token: str,
    author: str = "",
) -> list[dict]:
    """`/repos/{owner_repo}/commits` — 오늘 (KST) 그 repo 의 author commits (spec-03 §2.4).

    `/users/{user}/events` 의 PushEvent payload.commits 가 GitHub API 변경으로 빈 배열로 바뀜 →
    repo commits endpoint 직접 호출로 전환.

    빈 token 이면 skip. 404/403 (권한 없는 repo) 도 silently skip.
    Returns: [{"repo": "...", "msg": "..."}, ...]
    """
    if not token or not owner_repo:
        return []

    since = f"{today.isoformat()}T00:00:00+09:00"
    until = f"{(today + timedelta(days=1)).isoformat()}T00:00:00+09:00"

    params: dict[str, str] = {"since": since, "until": until, "per_page": "100"}
    if author:
        params["author"] = author

    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(
                f"https://api.github.com/repos/{owner_repo}/commits",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github+json",
                },
                params=params,
            )
            if r.status_code in (403, 404, 409):
                # 권한 없거나 빈 repo — 다른 token 시도 가능. silently skip.
                return []
            r.raise_for_status()
            commits = r.json()
    except httpx.HTTPError as e:
        logger.warning("repo commits fetch failed for %s: %s", owner_repo, e)
        return []

    return [
        {"repo": owner_repo, "msg": c.get("commit", {}).get("message", "")}
        for c in commits
        if isinstance(c, dict)
    ]
