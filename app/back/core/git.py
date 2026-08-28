"""원장 레포 git 조작 — 승인 착지(inbox.md Step 5)의 pull · add · commit · push.

**순서가 계약이다: pull → write → add · commit · push.** pull 은 파일을 쓰기 전에
끝나 있어야 한다(`pull_ledger`) — 이유는 그 함수 주석에 있다.

케이스 1 정본: 파일이 먼저 착지하고, **푸시가 성공해야 DB 를 확정한다.**
dry-run(JOB_GIT_PUSH_DRY_RUN=1, dev)은 **여기까지 안 온다** — 커밋·푸시 둘 다
안 하고 md 파일만 워킹트리에 쓴다(사용자 결정 2026-08-25). 분기는
gate_service._land_and_push 가 한다 — 여기는 항상 실 커밋·푸시다.

여기는 git 만 안다 — 어떤 파일을 왜 쓰는지, 신원·자격을 어디서 가져오는지는
service(gate_service)의 몫이다.

신원·자격 규약:
- 커밋 author/committer 는 `-c user.name=… -c user.email=…` 로 명령 단위 주입 —
  전역 gitconfig 를 오염시키지 않는다.
- push 자격(토큰)은 **환경변수 + credential helper** 로만 전달한다 — 원격 URL 을
  바꿔치기하지 않고, argv·로그·git 설정 어디에도 토큰이 남지 않는다.
"""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class GitPushError(Exception):
    """pull·commit·push 어느 단계든 실패 — 게이트는 approved + commit_ref NULL 로 남는다."""


@dataclass(frozen=True)
class GitIdentity:
    """착지 커밋 신원 — git_token personal 행의 account·email (사용자 결정)."""

    name: str    # git_token.account
    email: str   # git_token.email


@dataclass(frozen=True)
class GitPushCredentials:
    """https push 자격 — git_token personal 행의 account + 복호한 토큰."""

    account: str
    token: str


@dataclass(frozen=True)
class GitPushResult:
    sha: str            # 확정 HEAD — gate.commit_ref 에 적힌다
    committed: bool     # False 면 변경 없음(재시도에서 이미 착지한 경우) — HEAD 재사용


async def _run(
    cwd: str, *args: str, env: dict[str, str] | None = None
) -> tuple[int, str]:
    # safe.directory — 컨테이너(root)가 호스트 소유의 /ledger 마운트를 만질 때
    # dubious-ownership 거부를 피한다. 명령줄 -c 는 protected config 라 유효하다.
    proc = await asyncio.create_subprocess_exec(
        "git", "-C", cwd, "-c", f"safe.directory={cwd}", *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        env=env,
    )
    out, _ = await proc.communicate()
    return proc.returncode or 0, out.decode(errors="replace").strip()


# 자격을 env 로 읽는 helper — 토큰이 argv 에 실리지 않는다.
_CRED_HELPER = (
    '!f() { echo "username=${KKNAKS_GIT_PUSH_USER}"; '
    'echo "password=${KKNAKS_GIT_PUSH_TOKEN}"; }; f'
)


async def _resolve_push_target(ledger: str) -> tuple[str, str]:
    """(https push URL, 현재 브랜치). ssh 원격(git@github.com:…)은 https 로 바꿔 쓴다
    — 원격 설정 자체는 건드리지 않고 실행 시점 인자로만 쓴다."""
    code, url = await _run(ledger, "remote", "get-url", "--push", "origin")
    if code != 0 or not url:
        raise GitPushError(f"git 원격(origin) 조회 실패: {url or code}")
    if url.startswith("git@github.com:"):
        url = "https://github.com/" + url.removeprefix("git@github.com:")
    if not url.startswith("https://"):
        raise GitPushError(f"https 로 push 할 수 없는 원격입니다: {url}")

    code, branch = await _run(ledger, "rev-parse", "--abbrev-ref", "HEAD")
    if code != 0 or not branch or branch == "HEAD":
        raise GitPushError(f"현재 브랜치 확인 실패(detached?): {branch or code}")
    return url, branch


def _push_env(credentials: GitPushCredentials) -> dict[str, str]:
    return {
        **os.environ,
        "KKNAKS_GIT_PUSH_USER": credentials.account,
        "KKNAKS_GIT_PUSH_TOKEN": credentials.token,
    }


async def pull_ledger(
    ledger: str,
    identity: GitIdentity,
    *,
    credentials: GitPushCredentials | None = None,
) -> None:
    """착지 파일을 **쓰기 전에** 원격을 당긴다. 실패면 GitPushError.

    pull 은 --rebase — 사람이 옵시디언에서 같은 레포를 밀기 때문(inbox.md Step 7).
    그 이상의 동기화 장치는 두지 않는다.

    **신원이 여기도 필요하다** (2026-08-28 게이트 43 실사고):
    푸시가 실패해 로컬 커밋이 남은 상태에서 재시도하면 rebase 가 커밋을 새로 만든다.
    컨테이너에는 전역 gitconfig 가 없어 `unable to auto-detect email address
    (root@<컨테이너>.(none))` 로 죽는다 — 「커밋은 됐는데 푸시가 실패」한 게이트의
    복구 경로가 통째로 막힌다. 평소엔 로컬 커밋이 없어 fast-forward 라 안 걸렸다.
    commit 과 같은 방식으로 명령 단위 주입한다.

    **왜 write 앞인가** (2026-08-28 실사고, 게이트 29·43):
    `git pull --rebase` 는 tracked 파일에 스테이징 안 된 변경이 있으면 fetch 전에
    거부한다. 착지가 파일을 먼저 쓰면 **자기가 쓴 파일이 자기 pull 을 막는다** —
    기존 개념 파일을 보강하는 게이트 2 는 그래서 한 번도 착지하지 못했다(새 파일을
    만드는 게이트 1 은 untracked 라 우연히 통과했다). 게다가 실패한 파일이 워킹트리에
    남아 **그 뒤의 모든 착지가 같이 죽었다.**

    pull 을 앞에 두면 실패해도 워킹트리가 그대로다 — 재시도가 깨끗하고, 실패가
    다음 게이트로 번지지 않는다.
    """
    if credentials is None:
        raise GitPushError("push 자격이 없습니다 — personal 토큰을 등록하세요")
    # pull 도 push 와 같은 자격을 쓴다 — 컨테이너에는 저장된 자격이 없다.
    url, branch = await _resolve_push_target(ledger)
    code, out = await _run(
        ledger, "-c", "credential.helper=",  # 저장된 helper 무시 — 이 자격만 쓴다
        "-c", f"credential.helper={_CRED_HELPER}",
        "-c", f"user.name={identity.name}",   # rebase 가 커밋을 만들 수 있다
        "-c", f"user.email={identity.email}",
        "pull", "--rebase", url, branch, env=_push_env(credentials),
    )
    if code != 0:
        raise GitPushError(f"git pull 실패: {out.splitlines()[-1] if out else code}")


async def commit_and_push(
    ledger: str,
    paths: list[str],
    message: str,
    identity: GitIdentity,
    *,
    credentials: GitPushCredentials | None = None,
) -> GitPushResult:
    """add(파일 단위) → commit → push. 어느 단계든 실패면 GitPushError.

    **pull 은 여기서 하지 않는다** — 파일이 써지기 전에 `pull_ledger` 로 끝나 있어야
    한다(호출자 책임). 이유는 `pull_ledger` 주석.

    - add 는 **넘겨받은 경로만** — 워킹트리의 다른 변경이 커밋에 섞이면 안 된다.
    - 변경이 없으면(푸시 실패 재시도에서 파일이 이미 같음) 커밋을 만들지 않고
      HEAD 를 그대로 쓴다 — 게이트 하나 = 커밋 하나가 유지된다.
    """
    if credentials is None:
        raise GitPushError("push 자격이 없습니다 — personal 토큰을 등록하세요")
    push_url, branch = await _resolve_push_target(ledger)
    push_env = _push_env(credentials)

    code, out = await _run(ledger, "add", "--", *paths)
    if code != 0:
        raise GitPushError(f"git add 실패: {out.splitlines()[-1] if out else code}")

    code, _ = await _run(ledger, "diff", "--cached", "--quiet", "--", *paths)
    committed = False
    if code != 0:  # staged 변경 있음 → 커밋 (신원은 명령 단위 주입)
        code, out = await _run(
            ledger,
            "-c", f"user.name={identity.name}",
            "-c", f"user.email={identity.email}",
            "commit", "-m", message, "--only", "--", *paths,
        )
        if code != 0:
            raise GitPushError(f"git commit 실패: {out.splitlines()[-1] if out else code}")
        committed = True

    code, out = await _run(
        ledger, "-c", "credential.helper=",  # pull_ledger 와 동일 — 이 자격만 쓴다
        "-c", f"credential.helper={_CRED_HELPER}",
        "push", push_url, f"HEAD:{branch}", env=push_env,
    )
    if code != 0:
        raise GitPushError(f"git push 실패: {out.splitlines()[-1] if out else code}")

    code, sha = await _run(ledger, "rev-parse", "HEAD")
    if code != 0 or not sha:
        raise GitPushError("git rev-parse HEAD 실패")
    return GitPushResult(sha=sha, committed=committed)
