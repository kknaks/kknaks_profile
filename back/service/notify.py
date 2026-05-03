"""Slack incoming webhook 알림 — `SLACK_WEBHOOK_URL` env 박혀있으면 동작, 아니면 no-op.

잔디 잡 / 콘텐츠 enrich 잡 결과 알림 공통.
"""

from __future__ import annotations

import logging
import os

import httpx

logger = logging.getLogger("kknaks-back.notify")


async def notify_slack(text: str) -> None:
    """Slack incoming webhook POST. URL 미박음/네트워크 에러 시 silently skip — 잡 흐름 안 깨짐."""
    url = os.environ.get("SLACK_WEBHOOK_URL", "").strip()
    if not url:
        return
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.post(url, json={"text": text})
            if r.status_code >= 400:
                logger.warning("slack webhook %d: %s", r.status_code, r.text[:200])
    except Exception as e:  # noqa: BLE001
        logger.warning("slack notify failed: %s", e)
