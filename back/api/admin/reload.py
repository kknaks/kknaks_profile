"""POST /admin/reload — 페르소나 reload + content enrich 잡 트리거 (ADR-03 §4.2, spec-06 §1).

인증 두 모드 (둘 중 하나라도 통과하면 OK):
- GitHub webhook: X-Hub-Signature-256 (HMAC-SHA256, env `GITHUB_WEBHOOK_SECRET`)
- cron / 수동: X-Reload-Token (env `RELOAD_TOKEN`)

흐름 (push event 기준 — planning-01 §3.6 ② 채널):
1. ping event → pong (GitHub 가 webhook 등록 시 ping 한 번 보냄)
2. push event:
   - **self-push 필터** — payload `commits[*].author.email` 이 모두 `config.bot_emails()` 에 속하면 skip
     (서버 자기 push 가 다시 webhook 발화 → fetch/load_all/LLM init 비용 노이즈 방지)
   - `git pull --rebase origin main` (extraheader 인증, token argv 노출 회피)
   - `load_all()` (즉시 메모리 dict 갱신)
   - `run_content_enrich_job` (background — LLM 호출 60-120s, GitHub webhook 10s timeout 회피)
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import subprocess

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request

import config
from service.jobs.git_push import _build_auth_args, _redact_cmd
from service.jobs.inputs import REPO

logger = logging.getLogger("kknaks-back.admin-reload")

router = APIRouter()


def _verify_hmac(secret: str, signature_header: str | None, body: bytes) -> bool:
    """GitHub webhook HMAC-SHA256 검증. signature 형식: 'sha256=<hex>'."""
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    received = signature_header[len("sha256="):]
    return hmac.compare_digest(expected, received)


def _is_self_push(body: bytes) -> bool:
    """payload commits 가 모두 bot identity 의 commit 이면 True (self-push)."""
    bot_emails = config.bot_emails()
    if not bot_emails:
        return False
    try:
        payload = json.loads(body)
    except (ValueError, TypeError):
        return False
    commits = payload.get("commits") or []
    if not commits:
        return False
    return all(
        (c.get("author", {}).get("email") or "") in bot_emails
        for c in commits
    )


def _git_pull_rebase() -> None:
    """origin main 과 강제 동기화 (fetch + reset --hard).

    - extraheader 인증 (Basic + base64)
    - rebase 가 아니라 reset --hard — 호스트 working tree 가 origin 의 mirror.
      운영 모델: origin 이 SoT, 컨테이너가 git push 할 때만 일시적 변경.
      webhook 호출 시점에 dirty working tree 면 이전 push 가 incomplete 였거나 외부 수정 — 어느 쪽이든 origin 우선.
    - 실패 시 raise (호출자가 503 으로 응답 → GitHub webhook delivery 페이지에서 가시화).
    """
    identity = config.bot_identity()
    auth = _build_auth_args(identity["token"]) if identity else []
    try:
        subprocess.run(
            ["git", *auth, "fetch", "origin", "main"],
            cwd=REPO, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "reset", "--hard", "origin/main"],
            cwd=REPO, check=True, capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        cmd_safe = _redact_cmd(e.cmd if isinstance(e.cmd, list) else [e.cmd])
        stderr = (e.stderr or b"").decode("utf-8", errors="replace")[:500]
        logger.error(
            "git pull failed: cmd=%s exit=%d stderr=%s",
            cmd_safe, e.returncode, stderr,
        )
        raise


@router.post("/admin/reload")
async def reload(
    request: Request,
    background_tasks: BackgroundTasks,
    x_reload_token: str | None = Header(default=None),
    x_hub_signature_256: str | None = Header(default=None),
    x_github_event: str | None = Header(default=None),
):
    body = await request.body()

    webhook_secret = config.github_webhook_secret()
    expected_token = config.reload_token()

    is_authenticated = False
    if x_hub_signature_256 and webhook_secret:
        if _verify_hmac(webhook_secret, x_hub_signature_256, body):
            is_authenticated = True
    if not is_authenticated and x_reload_token and expected_token:
        if hmac.compare_digest(x_reload_token, expected_token):
            is_authenticated = True

    if not is_authenticated:
        raise HTTPException(403, "invalid auth")

    # GitHub ping event — webhook 등록 검증용
    if x_github_event == "ping":
        return {"status": "pong"}

    # self-push 필터 — 서버가 박은 commit 만 있는 push 는 skip
    if x_github_event == "push" and _is_self_push(body):
        logger.info("self-push detected — skip reload")
        return {"status": "skipped", "reason": "self-push"}

    # git pull (webhook 일 때만 — 수동 reload 는 호출자가 이미 pull 했다고 가정)
    if x_github_event == "push":
        try:
            _git_pull_rebase()
        except subprocess.CalledProcessError:
            raise HTTPException(503, "git pull failed")

    # 메모리 reload (즉시)
    from main import load_all

    load_all()

    # enrich 잡 — background (LLM 호출 60-120s 걸림 → GitHub webhook 10s timeout 회피)
    background_tasks.add_task(_run_enrich_safe)

    return {"status": "reloaded", "enrich": "queued"}


async def _run_enrich_safe() -> None:
    """background task — exception 잡혀도 logger 만 남기고 silently return."""
    from service.jobs.content_enrich import run_content_enrich_job

    try:
        n = await run_content_enrich_job()
        if n > 0:
            logger.info("content enrich done: %d processed", n)
    except Exception as e:
        logger.exception("content enrich failed: %s", e)
