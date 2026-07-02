"""Slack Socket Mode process for WORK-006 knowledge capture."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import httpx
import redis.asyncio as aioredis
import yaml

BACK_DIR = Path(__file__).resolve().parents[1] / "back"
if str(BACK_DIR) not in sys.path:
    sys.path.insert(0, str(BACK_DIR))

from open_kknaks import AgentClient, RedisBroker  # noqa: E402
from service.knowledge_capture import CaptureSessionStore  # noqa: E402
from service.slack_bridge import KnowledgeCaptureRunner, create_capture_app  # noqa: E402

KST = ZoneInfo("Asia/Seoul")


def _csv_env(name: str) -> set[str]:
    return {value.strip() for value in os.environ.get(name, "").split(",") if value.strip()}


def _known_stems(repo_root: Path) -> set[str]:
    try:
        graph = json.loads((repo_root / "_graph.json").read_text(encoding="utf-8"))
        return {str(node["id"]) for node in graph.get("nodes", [])}
    except (OSError, ValueError, KeyError):
        return set()


def _allowed_groups(repo_root: Path) -> set[str]:
    try:
        meta = yaml.safe_load((repo_root / "persona/_meta.yaml").read_text(encoding="utf-8"))
        return {str(item["id"]) for item in meta["notes"]["clusters"]}
    except (OSError, TypeError, KeyError):
        return {"study"}


async def main() -> None:
    if os.environ.get("SLACK_CAPTURE_ENABLED", "0") != "1":
        raise RuntimeError("SLACK_CAPTURE_ENABLED must be 1")
    bot_token = os.environ["SLACK_BOT_TOKEN"]
    app_token = os.environ["SLACK_APP_TOKEN"]
    reload_token = os.environ["RELOAD_TOKEN"]
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
    namespace = os.environ.get("NAMESPACE", "kknaks-portfolio")
    repo_root = Path(os.environ.get("REPO_ROOT", Path(__file__).resolve().parents[2])).resolve()
    backend_url = os.environ.get("BACKEND_URL", "http://back:48000").rstrip("/")

    broker = RedisBroker(url=redis_url, namespace=namespace)
    await broker.connect()
    redis = aioredis.from_url(redis_url, decode_responses=True)
    sessions = CaptureSessionStore(redis)

    async def reload_backend() -> bool:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                f"{backend_url}/admin/reload-data",
                headers={"X-Reload-Token": reload_token},
            )
            return response.status_code == 200

    runner = KnowledgeCaptureRunner(
        AgentClient(broker),
        sessions,
        repo_root=repo_root,
        provider=os.environ.get("CAPTURE_PROVIDER", "claude"),
        model=os.environ.get("CAPTURE_MODEL") or None,
        work_dir=os.environ.get("CAPTURE_WORK_DIR", "/repo"),
        known_stems=lambda: _known_stems(repo_root),
        allowed_groups=lambda: _allowed_groups(repo_root),
        reload_data=reload_backend,
        now=lambda: datetime.now(KST),
        timeout_seconds=float(os.environ.get("CAPTURE_TIMEOUT_SECONDS", "600")),
    )
    app = await create_capture_app(
        runner,
        sessions,
        bot_token=bot_token,
        allowed_users=_csv_env("ALLOWED_SLACK_USERS"),
        allowed_channels=_csv_env("ALLOWED_SLACK_CHANNELS"),
    )
    from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

    try:
        await AsyncSocketModeHandler(app, app_token).start_async()
    finally:
        await redis.aclose()
        await broker.close()


if __name__ == "__main__":
    asyncio.run(main())
