"""Slack Bolt handlers; business logic remains in the injected runner."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any, Protocol

from service.knowledge_capture.session import CaptureSessionStore

logger = logging.getLogger("kknaks-back.slack-capture")
MENTION_RE = re.compile(r"<@[A-Z0-9]+>\s*")
ALLOWED_SUBTYPES: set[str | None] = {None}


@dataclass(frozen=True)
class CaptureRequest:
    request_id: str
    entrypoint: str
    team_id: str
    channel_id: str
    user_id: str
    root_thread_ts: str
    text: str


class CaptureRunner(Protocol):
    async def handle(self, request: CaptureRequest, slack_client: Any) -> None: ...


def normalize_event(
    event: dict[str, Any],
    body: dict[str, Any],
    *,
    entrypoint: str,
) -> CaptureRequest:
    root_thread_ts = str(event.get("thread_ts") or event["ts"])
    text = MENTION_RE.sub("", str(event.get("text") or "")).strip()
    event_id = str(body.get("event_id") or f"{event.get('channel')}:{event.get('ts')}")
    return CaptureRequest(
        request_id=event_id,
        entrypoint=entrypoint,
        team_id=str(body.get("team_id") or event.get("team") or ""),
        channel_id=str(event["channel"]),
        user_id=str(event["user"]),
        root_thread_ts=root_thread_ts,
        text=text,
    )


async def create_capture_app(
    runner: CaptureRunner,
    sessions: CaptureSessionStore,
    *,
    bot_token: str,
    allowed_users: set[str],
    allowed_channels: set[str],
):
    """Create a Slack AsyncApp without starting its Socket Mode handler."""
    from slack_bolt.async_app import AsyncApp

    app = AsyncApp(token=bot_token)
    auth = await app.client.auth_test()
    bot_user_id = str(auth["user_id"])

    def authorized(event: dict[str, Any]) -> bool:
        if not allowed_users or not allowed_channels:
            return False
        return (
            event.get("user") in allowed_users
            and event.get("channel") in allowed_channels
        )

    async def dispatch(event, body, client, *, entrypoint: str) -> None:
        if not authorized(event):
            logger.info("ignored unauthorized Slack event user=%s channel=%s", event.get("user"), event.get("channel"))
            return
        request = normalize_event(event, body, entrypoint=entrypoint)
        if not request.text:
            return
        async with sessions.lock(request.channel_id, request.root_thread_ts):
            if not await sessions.claim_event(request.request_id):
                logger.info("ignored duplicate Slack event=%s", request.request_id)
                return
            await runner.handle(request, client)

    @app.event("app_mention")
    async def on_mention(event, body, client):
        await dispatch(event, body, client, entrypoint="app_mention")

    @app.event("message")
    async def on_message(event, body, client):
        if event.get("bot_id") or event.get("user") == bot_user_id:
            return
        if event.get("subtype") not in ALLOWED_SUBTYPES:
            return
        if f"<@{bot_user_id}>" in str(event.get("text") or ""):
            return
        thread_ts = event.get("thread_ts")
        if not thread_ts:
            return
        if await sessions.get(str(event["channel"]), str(thread_ts)) is None:
            return
        await dispatch(event, body, client, entrypoint="thread_message")

    return app
