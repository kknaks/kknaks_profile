"""Slack capture 웹소켓 supervisor 테스트 (KDEV-WORK-012).

흡수 전에는 루프가 죽으면 프로세스가 종료되고 compose `restart: unless-stopped` 가
컨테이너를 재시작해 캡처가 복구됐다. 흡수 후 back 은 살아 있어야 하므로 그 복구 경로가
사라졌고, `supervise_connection` 이 그 자리를 대신한다.
"""

from __future__ import annotations

import asyncio

import pytest

from service.slack_bridge.bootstrap import supervise_connection


class Clock:
    """단조 시계 fake — sleep 이 실제로 기다리지 않고 시간만 흐르게 한다."""

    def __init__(self) -> None:
        self.t = 0.0
        self.slept: list[float] = []

    def now(self) -> float:
        return self.t

    async def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)
        self.t += seconds

    def advance(self, seconds: float) -> None:
        self.t += seconds


@pytest.mark.asyncio
async def test_backoff_grows_and_gives_up_after_threshold():
    """즉시 죽는 연결은 지수 백오프로 재시도하다 임계를 넘으면 포기한다."""
    clock = Clock()
    attempts = 0

    async def connect():
        nonlocal attempts
        attempts += 1
        raise RuntimeError("socket dead")

    await supervise_connection(
        connect,
        sleep=clock.sleep,
        now=clock.now,
        base_delay=5.0,
        max_delay=40.0,
        max_consecutive=4,
        healthy_seconds=60.0,
    )

    # 4번 재기동하고 5번째 실패에서 포기 → connect 는 5회 호출된다
    assert attempts == 5
    # 5 → 10 → 20 → 40(상한) 으로 증가하고 상한을 넘지 않는다
    assert clock.slept == [5.0, 10.0, 20.0, 40.0]


@pytest.mark.asyncio
async def test_giveup_notifies_once():
    """포기는 조용히 일어나면 안 된다 — back 재시작 전까지 캡처가 멈춰 있다는 뜻이다."""
    clock = Clock()
    notified: list[str] = []

    async def connect():
        raise RuntimeError("dead")

    async def on_giveup(message: str) -> None:
        notified.append(message)

    await supervise_connection(
        connect,
        on_giveup=on_giveup,
        sleep=clock.sleep,
        now=clock.now,
        max_consecutive=2,
    )

    assert len(notified) == 1
    assert "재기동 실패" in notified[0]


@pytest.mark.asyncio
async def test_giveup_notify_failure_does_not_raise():
    """알림 실패가 supervisor 를 예외로 끝내지 않는다."""
    clock = Clock()

    async def connect():
        raise RuntimeError("dead")

    async def on_giveup(_message: str) -> None:
        raise RuntimeError("webhook down")

    await supervise_connection(
        connect,
        on_giveup=on_giveup,
        sleep=clock.sleep,
        now=clock.now,
        max_consecutive=1,
    )


@pytest.mark.asyncio
async def test_no_notify_when_cancelled():
    """정상 shutdown 은 장애가 아니므로 알리지 않는다."""
    clock = Clock()
    notified: list[str] = []

    async def connect():
        raise asyncio.CancelledError

    async def on_giveup(message: str) -> None:
        notified.append(message)

    with pytest.raises(asyncio.CancelledError):
        await supervise_connection(
            connect, on_giveup=on_giveup, sleep=clock.sleep, now=clock.now
        )

    assert notified == []


@pytest.mark.asyncio
async def test_healthy_run_resets_backoff():
    """오래 붙어 있다가 끊긴 경우는 과거 실패 이력을 끌고 가지 않는다."""
    clock = Clock()
    calls = 0

    async def connect():
        nonlocal calls
        calls += 1
        if calls <= 2:
            # 즉시 실패 — 백오프가 5 → 10 으로 자란다
            raise RuntimeError("flap")
        if calls == 3:
            # 오래 붙어 있다가 끊김
            clock.advance(3600)
            raise RuntimeError("long-lived disconnect")
        raise asyncio.CancelledError

    with pytest.raises(asyncio.CancelledError):
        await supervise_connection(
            connect,
            sleep=clock.sleep,
            now=clock.now,
            base_delay=5.0,
            max_delay=300.0,
            max_consecutive=10,
            healthy_seconds=60.0,
        )

    # 3번째(장시간 연결) 이후 대기가 상한이 아니라 base 로 돌아온다
    assert clock.slept == [5.0, 10.0, 5.0]


@pytest.mark.asyncio
async def test_cancel_propagates_and_does_not_restart():
    """shutdown 은 재기동 대상이 아니다 — 취소가 그대로 전파돼야 lifespan 이 끝난다."""
    clock = Clock()
    attempts = 0

    async def connect():
        nonlocal attempts
        attempts += 1
        raise asyncio.CancelledError

    with pytest.raises(asyncio.CancelledError):
        await supervise_connection(connect, sleep=clock.sleep, now=clock.now)

    assert attempts == 1
    assert clock.slept == []


@pytest.mark.asyncio
async def test_handler_is_closed_between_restarts():
    """죽은 핸들러를 정리하고 새로 만든다 — 이전 소켓 상태를 물고 들어가지 않게."""
    clock = Clock()
    closed = 0
    attempts = 0

    async def connect():
        nonlocal attempts
        attempts += 1
        raise RuntimeError("dead")

    async def close():
        nonlocal closed
        closed += 1

    await supervise_connection(
        connect,
        close=close,
        sleep=clock.sleep,
        now=clock.now,
        max_consecutive=2,
    )

    assert attempts == 3
    assert closed == 3


@pytest.mark.asyncio
async def test_close_failure_does_not_block_restart():
    """정리 실패가 재기동을 막지 않는다."""
    clock = Clock()
    attempts = 0

    async def connect():
        nonlocal attempts
        attempts += 1
        raise RuntimeError("dead")

    async def close():
        raise RuntimeError("close blew up")

    await supervise_connection(
        connect,
        close=close,
        sleep=clock.sleep,
        now=clock.now,
        max_consecutive=2,
    )

    assert attempts == 3


@pytest.mark.asyncio
async def test_clean_return_is_treated_as_disconnect():
    """예외 없이 반환해도 연결이 끊긴 것이므로 재기동한다."""
    clock = Clock()
    attempts = 0

    async def connect():
        nonlocal attempts
        attempts += 1
        return  # 조용히 반환

    await supervise_connection(
        connect,
        sleep=clock.sleep,
        now=clock.now,
        max_consecutive=2,
    )

    assert attempts == 3
