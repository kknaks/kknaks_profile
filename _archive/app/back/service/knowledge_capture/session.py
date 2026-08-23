"""Redis-backed Slack thread/session state and concurrency control."""

from __future__ import annotations

import json
import secrets
from contextlib import asynccontextmanager
from dataclasses import asdict, dataclass
from typing import AsyncIterator


@dataclass(frozen=True)
class CaptureSession:
    channel_id: str
    root_thread_ts: str
    session_id: str | None
    kind: str | None
    output_path: str | None
    first_prompt: str
    created_at: str
    last_seen_at: str
    #: 이 스레드가 만든 승인 큐 항목 (KDEV-WORK-014). 스레드에 덧붙는 말을 그 항목의
    #: 메모로 흘려보내기 위한 연결고리다. 기본값이 있어 이전 형식의 레코드도 그대로 읽힌다.
    item_id: int | None = None


class ThreadBusyError(RuntimeError):
    """Another event is already updating this Slack thread."""


class CaptureSessionStore:
    def __init__(
        self,
        redis,
        *,
        namespace: str = "kknaks-capture",
        ttl_seconds: int = 604800,
        lock_seconds: int = 900,
    ) -> None:
        self.redis = redis
        self.namespace = namespace
        self.ttl_seconds = ttl_seconds
        self.lock_seconds = lock_seconds

    def _session_key(self, channel_id: str, root_thread_ts: str) -> str:
        return f"{self.namespace}:session:{channel_id}:{root_thread_ts}"

    def _event_key(self, event_id: str) -> str:
        return f"{self.namespace}:event:{event_id}"

    def _lock_key(self, channel_id: str, root_thread_ts: str) -> str:
        return f"{self.namespace}:lock:{channel_id}:{root_thread_ts}"

    async def get(self, channel_id: str, root_thread_ts: str) -> CaptureSession | None:
        raw = await self.redis.get(self._session_key(channel_id, root_thread_ts))
        if raw is None:
            return None
        if isinstance(raw, bytes):
            raw = raw.decode()
        return CaptureSession(**json.loads(raw))

    async def set(self, session: CaptureSession) -> None:
        await self.redis.set(
            self._session_key(session.channel_id, session.root_thread_ts),
            json.dumps(asdict(session), ensure_ascii=False, separators=(",", ":")),
            ex=self.ttl_seconds,
        )

    async def claim_event(self, event_id: str) -> bool:
        """Return True only for the first delivery of an event."""
        return bool(await self.redis.set(
            self._event_key(event_id),
            "1",
            ex=self.ttl_seconds,
            nx=True,
        ))

    @asynccontextmanager
    async def lock(self, channel_id: str, root_thread_ts: str) -> AsyncIterator[None]:
        key = self._lock_key(channel_id, root_thread_ts)
        token = secrets.token_hex(16)
        acquired = await self.redis.set(key, token, ex=self.lock_seconds, nx=True)
        if not acquired:
            raise ThreadBusyError(f"capture thread is busy: {channel_id}/{root_thread_ts}")
        try:
            yield
        finally:
            # Delete only our lock; an expired/reacquired lock belongs to another worker.
            await self.redis.eval(
                "if redis.call('get', KEYS[1]) == ARGV[1] "
                "then return redis.call('del', KEYS[1]) else return 0 end",
                1,
                key,
                token,
            )
