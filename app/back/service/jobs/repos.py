"""bare 클론 관리 — 클론·fetch·실패 표시 (KDEV-WORK-017 P5 / KDEV-SPEC-011 S-1 2~4항).

조사는 **서버에 클론한 bare 레포**를 읽는다. GitHub API 로는 default branch 밖의
커밋을 볼 수 없어 실측 17.3%(본인 커밋 7.9%)가 누락되기 때문이다(BL-004).

여기서 하는 일은 셋이다 — 없으면 클론하고, 있으면 fetch 하고, 실패를 레지스트리에
남긴다. **커밋을 읽는 것은 이 모듈이 아니다**(`collect_commits.py`). 클론 상태와
조사를 나눈 이유는 실패 처리가 다르기 때문이다 — fetch 실패는 그 레포만 건너뛰고
조사는 계속한다(S-1 4항).
"""

from __future__ import annotations

import asyncio
import logging
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

import config
import repository.tracked_repos as tracked_repos_repo
from service.notify import notify_slack
from service.products.dto import TrackedRepoDTO

# `_build_auth_args` 는 이름만 private 이고 이미 `apply/git.py`·`admin/reload.py` 가
# 같은 방식으로 가져다 쓴다. git-over-HTTPS 인증은 한 군데서만 조립해야 하는 값이라
# 여기서 다시 만들지 않는다.
from service.jobs.git_push import _build_auth_args

logger = logging.getLogger("kknaks-back.repos")

#: SPEC-011 §4 Case Matrix 의 코드. 그대로 `last_error` 와 Slack 문구에 실린다.
CODE_TOKEN_MISSING = "TOKEN_MISSING"
CODE_CLONE_FAILED = "CLONE_FAILED"
CODE_FETCH_FAILED = "FETCH_FAILED"

#: 전 브랜치를 받는다. `git clone --bare` 는 **fetch refspec 을 남기지 않아**
#: 그냥 두면 이후 fetch 가 새 브랜치를 가져오지 않는다 — `_configure_refspec` 참조.
_ALL_BRANCHES = "+refs/heads/*:refs/heads/*"


@dataclass(frozen=True)
class SyncResult:
    """레포 하나의 클론·fetch 결과. 실패해도 예외를 던지지 않는다 — 부분 실패는 정상이다."""

    slug: str
    ok: bool
    path: Path | None = None
    code: str | None = None
    message: str = ""


def clone_dir(slug: str, root: Path | None = None) -> Path:
    """`owner/name` → 클론 경로.

    `owner__name.git` 으로 **평평하게** 둔다. `owner/name.git` 으로 중첩시키면 owner
    디렉터리가 빈 채로 남아 정리 대상이 하나 늘고, 얻는 것은 없다.
    """
    root = root or config.repo_cache_dir()
    return root / (slug.replace("/", "__") + ".git")


def clone_url(slug: str) -> str:
    """`owner/name` → 클론 URL. 토큰은 URL 에 넣지 않는다 — extraheader 로 넘긴다."""
    return f"{config.github_clone_base()}{slug}.git"


def assert_outside_worktree(root: Path) -> None:
    """클론 루트가 레포 작업트리 **밖**인지 확인한다 (SPEC-011 §5 「클론 위치」).

    안에 있으면 발행 경로의 작업트리 초기화가 클론을 지운다. 조용히 지워지면 다음
    조사가 321MB 를 다시 받으므로, **돌기 전에 멈추는 편이 싸다.**
    """
    repo_root = config.repo_root().resolve()
    resolved = root.resolve()
    if resolved == repo_root or repo_root in resolved.parents:
        raise RuntimeError(
            f"클론 루트가 레포 작업트리 안이다 — {resolved}. "
            "REPO_CACHE_DIR 을 작업트리 밖으로 옮겨야 한다 (SPEC-011 §5)"
        )


def _scrub(text: str, token: str | None) -> str:
    """토큰이 stderr 를 타고 `last_error`·Slack 으로 새는 것을 막는다.

    인증은 extraheader 로 넘기므로 URL 에는 토큰이 없지만, 그것은 **우리 쪽 사정**이고
    git 이 무엇을 출력할지는 우리가 정하지 않는다. 저장 직전에 한 번 지운다.
    """
    if token and token in text:
        text = text.replace(token, "<redacted>")
    return text.strip()[:500]


def _is_bare_clone(path: Path) -> bool:
    """이미 쓸 수 있는 bare 클론인지. 깨진 디렉터리를 fetch 대상으로 삼지 않는다."""
    if not path.is_dir():
        return False
    probe = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--is-bare-repository"],
        capture_output=True,
        text=True,
        check=False,
    )
    return probe.returncode == 0 and probe.stdout.strip() == "true"


def _configure_refspec(path: Path) -> None:
    """`remote.origin.fetch` 를 전 브랜치로 박는다.

    **`git clone --bare` 는 refspec 을 설정하지 않는다.** 그대로 두면 이후
    `fetch` 가 `FETCH_HEAD` 만 갱신하고 `refs/heads/*` 는 클론 당시에 멈춘다 —
    `git log --all` 이 **첫날 이후의 새 브랜치를 영영 못 본다**는 뜻이고, 전 브랜치를
    보려고 API 를 버린 이 파이프라인에서는 조용한 실패다.

    `--mirror` 로 클론하면 refspec 이 `+refs/*:refs/*` 라 GitHub 이 광고하는
    `refs/pull/*` 까지 받아 디스크가 불어난다. 우리가 필요한 것은 브랜치뿐이다.
    """
    subprocess.run(
        ["git", "-C", str(path), "config", "remote.origin.fetch", _ALL_BRANCHES],
        capture_output=True,
        text=True,
        check=True,
    )


def sync_repo(slug: str, account: str, *, root: Path | None = None) -> SyncResult:
    """레포 하나를 클론하거나 fetch 한다. **블로킹이다** — 호출자가 스레드로 뺀다.

    토큰이 없으면 **시도하지 않는다**(SPEC-011 §5 「토큰」). 공개 레포는 토큰 없이도
    받아지지만, 그러면 어느 레포가 어느 계정으로 받아졌는지가 상황에 따라 달라진다.
    """
    root = root or config.repo_cache_dir()
    assert_outside_worktree(root)

    token = config.gh_token(account)
    if not token:
        return SyncResult(
            slug=slug,
            ok=False,
            code=CODE_TOKEN_MISSING,
            message=f"{account} 토큰 미설정",
        )

    path = clone_dir(slug, root)
    auth = _build_auth_args(token)
    timeout = config.git_timeout_seconds()
    fresh = not _is_bare_clone(path)

    if fresh and path.exists():
        # 지우지 않는다. 조사는 읽기 전용이고(SPEC-011 §5 「멱등성」), 일시적 이상으로
        # 수백 MB 를 날리는 쪽이 사람이 한 번 보는 것보다 비싸다.
        return SyncResult(
            slug=slug,
            ok=False,
            code=CODE_CLONE_FAILED,
            message=f"{path} 가 bare 클론이 아니다 — 사람이 확인해야 한다",
        )

    try:
        if fresh:
            root.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["git", *auth, "clone", "--bare", clone_url(slug), str(path)],
                capture_output=True,
                text=True,
                check=True,
                timeout=timeout,
            )
            _configure_refspec(path)
        else:
            # 이미 있는 클론에도 매번 박는다 — 앞선 버전이 refspec 없이 만들어 두었을 수
            # 있고, 그 상태는 겉으로 정상처럼 보인다.
            _configure_refspec(path)
            subprocess.run(
                ["git", "-C", str(path), *auth, "fetch", "--all", "--prune"],
                capture_output=True,
                text=True,
                check=True,
                timeout=timeout,
            )
    except subprocess.TimeoutExpired:
        code = CODE_CLONE_FAILED if fresh else CODE_FETCH_FAILED
        return SyncResult(slug=slug, ok=False, code=code, message=f"{timeout:.0f}초 초과")
    except subprocess.CalledProcessError as exc:
        code = CODE_CLONE_FAILED if fresh else CODE_FETCH_FAILED
        return SyncResult(
            slug=slug, ok=False, code=code, message=_scrub(exc.stderr or "", token)
        )

    return SyncResult(slug=slug, ok=True, path=path)


async def sync_all(
    db: AsyncSession, repos: list[TrackedRepoDTO], *, root: Path | None = None
) -> list[SyncResult]:
    """레지스트리 항목들을 순서대로 동기화하고 결과를 레지스트리에 남긴다.

    **순차로 돈다.** 병렬은 디스크와 `WORKER_CONCURRENCY` 양쪽에 부딪히는데 이득이
    실측되지 않았다 — 발주서 Open Issue 「`investigate` 순차 13회 실측」과 같은 자리다.

    실패한 레포는 결과에서 `ok=False` 로 남고 **예외는 올라가지 않는다.** 하나의 실패가
    나머지를 막지 않는 것이 이 함수의 계약이다(SPEC-011 §5 「부분 실패」).

    **DTO 를 받고 상태 기록은 repository 에 맡긴다** (KDEV-WORK-018 P2). 종전에는 ORM
    객체를 받아 `repo.last_fetched_at` 을 직접 대입했는데, 그러면 ORM 이 도메인 코드로
    새어 세션 수명과 lazy load 를 이 함수가 알아야 한다.
    """
    results: list[SyncResult] = []
    now = datetime.now(timezone.utc)

    for repo in repos:
        result = await asyncio.to_thread(sync_repo, repo.slug, repo.account, root=root)
        results.append(result)
        if result.ok:
            await tracked_repos_repo.mark_synced(db, repo.id, now)
        else:
            await tracked_repos_repo.mark_failed(
                db, repo.id, result.code or "FETCH_FAILED", result.message
            )
            logger.warning("레포 동기화 실패 — %s (%s)", repo.slug, result.code)

    await _notify_failures(results)
    return results


async def _notify_failures(results: list[SyncResult]) -> None:
    """U-1 — 실패를 **한 메시지로 묶어** 알린다. 13개가 한꺼번에 죽으면 13통이 온다."""
    failed = [r for r in results if not r.ok]
    if not failed:
        return
    lines = [f":warning: 레포 조사 실패 — {len(failed)}건"]
    lines += [f"• `{r.slug}` {r.code}: {r.message}" for r in failed]
    await notify_slack("\n".join(lines))
