"""POST /admin/reload — 페르소나 reload + content enrich 잡 트리거 (ADR-03 §4.2, spec-06 §1).

인증 두 모드 (둘 중 하나라도 통과하면 OK):
- GitHub webhook: X-Hub-Signature-256 (HMAC-SHA256, env `GITHUB_WEBHOOK_SECRET`)
- cron / 수동: X-Reload-Token (env `RELOAD_TOKEN`)

흐름:
1. ping event → pong (GitHub 가 webhook 등록 시 ping 한 번 보냄)
2. push 또는 manual → load_all() (즉시) + run_content_enrich_job (background — LLM 호출 60-120s)
"""

from __future__ import annotations

import hashlib
import hmac
import logging

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request

import config

logger = logging.getLogger("kknaks-back.admin-reload")

router = APIRouter()


def _verify_hmac(secret: str, signature_header: str | None, body: bytes) -> bool:
    """GitHub webhook HMAC-SHA256 검증. signature 형식: 'sha256=<hex>'."""
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    received = signature_header[len("sha256="):]
    return hmac.compare_digest(expected, received)


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
