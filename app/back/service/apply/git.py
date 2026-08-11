"""원자적 발행 — 한 커밋, 실패하면 전량 롤백 (KDEV-WORK-015 P4 / KDEV-DEC-012 D3·D5).

기존 `commit_and_push_with_retry` 를 쓰지 않는 이유는 **롤백이 없기** 때문이다. 그
함수는 commit → rebase → push 순서로 가고, push 가 실패하면 로컬 커밋이 남는다.
그 상태를 두면 다음 `POST /admin/reload` 의 `git reset --hard origin/main` 이 그 커밋을
**조용히 삭제**한다 — 승인한 것이 사라졌는데 아무도 모른다.

여기서는 실패하면 **원래 커밋으로 되돌린다.** 서버가 항상 origin 과 같은 상태이거나,
아니면 발행이 끝난 상태 둘 중 하나만 되게 한다.
"""

from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path

import config

logger = logging.getLogger("kknaks-back.apply.git")


@dataclass(frozen=True)
class PublishOutcome:
    ok: bool
    commit_ref: str | None = None
    error_code: str | None = None
    error_message: str | None = None
    dry_run: bool = False


def _run(args: list[str], repo_root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=repo_root, check=True, capture_output=True)


def head_ref(repo_root: Path) -> str:
    return _run(["git", "rev-parse", "HEAD"], repo_root).stdout.decode().strip()


def _auth_args(token: str) -> list[str]:
    from service.jobs.git_push import _build_auth_args

    return _build_auth_args(token)


def publish_atomic(
    paths: list[str],
    message: str,
    *,
    repo_root: Path,
    dry_run: bool = True,
) -> PublishOutcome:
    """`paths` 를 **한 커밋**으로 묶어 push 한다. 어느 단계에서 실패하든 원래 상태로 되돌린다.

    한 커밋인 이유(DEC-012 D3): 나눠 커밋하면 중간 커밋에 **깨진 링크**가 남는다 —
    reference 만 들어간 커밋에서 concept 가 가리키는 대상이 없다.
    """
    before = head_ref(repo_root)

    if dry_run:
        logger.info("dry_run — 커밋/푸시 생략 (paths=%s, message=%r)", paths, message)
        return PublishOutcome(ok=True, commit_ref=None, dry_run=True)

    identity = config.bot_identity()
    if identity is None:
        # **여기서도 되돌린다.** 호출자는 이미 작업트리에 파일을 써 놓고 들어온다 —
        # 그냥 실패로 돌아가면 커밋되지 않은 산출물이 남고, 다음 `reset --hard` 가
        # 조용히 지울 때까지 미완성 트리가 보인다. "어느 단계에서 실패하든 원래
        # 상태로" 가 이 함수의 계약이고, 설정 누락도 그 단계 중 하나다.
        rollback(repo_root, before)
        return PublishOutcome(
            ok=False,
            error_code="BOT_IDENTITY_MISSING",
            error_message="GH_USER/TOKEN/EMAIL 미설정 — 발행할 수 없다",
        )

    auth = _auth_args(identity["token"])
    author = [
        "-c", f"user.email={identity['email']}",
        "-c", f"user.name={identity['user']}",
    ]

    try:
        _run(["git", "add", "--", *paths], repo_root)
        staged = subprocess.run(
            ["git", "diff", "--cached", "--quiet", "--", *paths], cwd=repo_root
        )
        if staged.returncode == 0:
            # 쓸 내용이 이미 그대로면 커밋할 것이 없다. 실패가 아니다.
            return PublishOutcome(ok=True, commit_ref=before)

        _run(["git", *author, "commit", "-m", message], repo_root)
        _run(["git", *auth, "fetch", "origin"], repo_root)
        _run(["git", "-c", "rebase.autoStash=true", "rebase", "origin/main"], repo_root)
        _run(["git", *auth, "push", "origin", "main"], repo_root)
        return PublishOutcome(ok=True, commit_ref=head_ref(repo_root))

    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or b"").decode("utf-8", errors="replace")[:500]
        logger.error("발행 실패 — 되돌린다: %s", stderr)
        rollback(repo_root, before)
        return PublishOutcome(
            ok=False,
            error_code="GIT_FAILED",
            error_message=stderr or "git 명령이 실패했다",
        )


def rollback(repo_root: Path, to_ref: str) -> None:
    """작업트리와 커밋을 `to_ref` 상태로 되돌린다.

    `reset --hard` 는 **추적되지 않는 파일을 지우지 않는다.** 커밋 전에 실패했다면
    새로 쓴 md 가 untracked 로 남으므로 `clean -fd` 까지 해야 origin 상태가 된다.

    정리 자체가 실패해도 예외를 올리지 않는다 — 롤백 실패로 발행 실패 기록까지
    잃으면 사람이 상황을 알 방법이 없어진다. 로그만 남긴다.
    """
    for args in (
        ["git", "rebase", "--abort"],
        ["git", "reset", "--hard", to_ref],
        ["git", "clean", "-fd"],
    ):
        try:
            subprocess.run(args, cwd=repo_root, check=False, capture_output=True)
        except Exception:  # noqa: BLE001
            logger.exception("롤백 명령 실패 (계속): %s", args)
