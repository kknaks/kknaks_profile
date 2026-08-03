"""Slack 캡처 런타임 조립 — back lifespan 에서 기동한다 (KDEV-WORK-012 / KDEV-DEC-013).

종전에는 `app/slack_bridge/run.py` 가 별도 컨테이너에서 이 조립을 했다. Socket Mode 는
아웃바운드 웹소켓이라 포트가 필요 없고, back 은 이미 `--workers 1` 하드락 위에서
APScheduler 라는 장기 asyncio 루프를 돌리고 있어 프로세스를 나눌 이유가 없었다.

흡수의 실질 이득은 **쓰기 소유권이 한 프로세스로 모이는 것**이다 — 별도 프로세스일 때는
bridge 가 파일을 쓰고 git push 까지 직접 했고, Postgres 에는 붙지 못했다.
"""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime
from typing import Awaitable, Callable
from zoneinfo import ZoneInfo

import config
from core.db import new_session
from service.knowledge_capture import CaptureSessionStore
from service.knowledge_capture.source import fetch_source
from service.pipeline import runtime
from service.pipeline.collect_git import GitCollect
from service.pipeline.driver import PipelineDriver
from service.pipeline.slack_intake import QueueIntakeRunner
from service.pipeline.route import RouteProposer
from service.pipeline.stages import ConceptStage, DerivedStage, SourceNoteStage
from service.pipeline.stages.daily import DailyStage
from service.pipeline.stages.investigate import AgentInvestigate
from service.pipeline.summarize import AgentSummarizer
from service.slack_bridge.app import create_capture_app

logger = logging.getLogger("kknaks-back.slack-capture")

KST = ZoneInfo("Asia/Seoul")

# 웹소켓 루프 재기동 정책.
# 흡수 전에는 루프가 죽으면 프로세스가 종료되고 compose `restart: unless-stopped` 가
# 컨테이너를 재시작해 캡처가 복구됐다. 흡수 후에는 back 이 살아 있어야 하므로(사이트 API)
# 그 복구 경로가 사라졌다 — 이 supervisor 가 그 자리를 대신한다.
RESTART_BASE_DELAY = 5.0
RESTART_MAX_DELAY = 300.0
RESTART_MAX_CONSECUTIVE = 10
HEALTHY_RUN_SECONDS = 60.0


async def supervise_connection(
    connect: Callable[[], Awaitable[None]],
    *,
    close: Callable[[], Awaitable[None]] | None = None,
    on_giveup: Callable[[str], Awaitable[None]] | None = None,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
    now: Callable[[], float] = time.monotonic,
    base_delay: float = RESTART_BASE_DELAY,
    max_delay: float = RESTART_MAX_DELAY,
    max_consecutive: int = RESTART_MAX_CONSECUTIVE,
    healthy_seconds: float = HEALTHY_RUN_SECONDS,
) -> None:
    """`connect()` 를 돌리다 끝나면 지수 백오프 후 재기동한다.

    - 취소(shutdown)는 그대로 전파한다 — 재기동하지 않는다.
    - `healthy_seconds` 이상 붙어 있었으면 "한 번 정상 동작했다"로 보고 백오프를 초기화한다.
      그래야 몇 시간 뒤의 단발 끊김이 과거 실패 이력 때문에 5분씩 기다리지 않는다.
    - 연속 실패가 `max_consecutive` 를 넘으면 포기한다. 토큰 폐기·앱 삭제처럼 재시도로
      풀리지 않는 상황에서 Slack API 를 무한히 두드리지 않기 위해서다.
    - 포기하면 `on_giveup` 으로 알린다. **조용히 죽는 경로를 남기지 않는다** — 이 상태는
      back 재시작 전까지 캡처가 멈춰 있다는 뜻이라 사람이 알아야 한다.
    """
    consecutive = 0
    delay = base_delay

    while True:
        started = now()
        try:
            await connect()
            logger.warning("Slack capture 연결이 반환됨 (예외 없음)")
        except asyncio.CancelledError:
            if close is not None:
                await _quiet(close())
            raise
        except Exception:
            logger.exception("Slack capture 연결이 예외로 끊김")

        if close is not None:
            await _quiet(close())

        if now() - started >= healthy_seconds:
            # 충분히 오래 붙어 있었으면 이번 끊김은 새 장애로 센다.
            consecutive = 0
            delay = base_delay

        consecutive += 1
        if consecutive > max_consecutive:
            message = (
                f"Slack capture 연속 {max_consecutive}회 재기동 실패 — 포기한다. "
                "복구하려면 back 재시작 필요"
            )
            logger.error(message)
            if on_giveup is not None:
                await _quiet(on_giveup(message))
            return

        logger.warning(
            "Slack capture %.0fs 후 재기동 (연속 실패 %d/%d)",
            delay,
            consecutive,
            max_consecutive,
        )
        await sleep(delay)
        delay = min(delay * 2, max_delay)


async def _quiet(awaitable) -> None:
    """종료/정리 경로의 예외는 삼킨다 — 재기동을 막을 이유가 없다."""
    try:
        await awaitable
    except asyncio.CancelledError:
        raise
    except Exception:  # noqa: BLE001
        logger.debug("Slack capture 정리 중 예외 (무시)", exc_info=True)


class CaptureRuntime:
    """Socket Mode 핸들러와 그 의존(broker·redis)의 수명을 lifespan 에 묶는다."""

    def __init__(self) -> None:
        self._task: asyncio.Task | None = None
        self._broker = None
        self._redis = None
        self._driver: PipelineDriver | None = None

    async def start(self) -> bool:
        """캡처를 기동한다. 설정이 없으면 조용히 skip 하고 False 를 반환한다.

        부팅을 막지 않는 것이 원칙이다 — 지식 캡처가 안 뜬다고 사이트 API 가 죽을 이유가 없다.
        """
        if not config.slack_capture_enabled():
            logger.info("Slack capture disabled (SLACK_CAPTURE_ENABLED=0)")
            return False

        bot_token = config.slack_bot_token()
        app_token = config.slack_app_token()
        if not (bot_token and app_token):
            logger.warning("Slack capture enabled but SLACK_BOT_TOKEN/SLACK_APP_TOKEN missing — skip")
            return False

        try:
            await self._build_and_start(bot_token, app_token)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Slack capture 기동 실패 — 캡처만 비활성화하고 API 는 계속 서빙")
            await self.stop()
            # 부팅 시 조용히 꺼지면 "왜 캡처가 안 되지"를 한참 뒤에 알게 된다.
            from service.notify import notify_slack

            await _quiet(notify_slack(
                f":electric_plug: Slack capture 기동 실패 — 캡처 비활성 (API 는 정상). "
                f"`{type(exc).__name__}: {str(exc)[:200]}`"
            ))
            return False
        return True

    async def _build_and_start(self, bot_token: str, app_token: str) -> None:
        import redis.asyncio as aioredis
        from open_kknaks import AgentClient, RedisBroker

        self._broker = RedisBroker(url=config.redis_url(), namespace=config.capture_namespace())
        await self._broker.connect()
        self._redis = aioredis.from_url(config.redis_url(), decode_responses=True)
        sessions = CaptureSessionStore(self._redis)

        # Slack 입력은 이제 **큐 항목 하나**가 된다 (KDEV-WORK-014 P2).
        # 파일 쓰기도 git push 도 여기서 일어나지 않는다 — 노트는 route 승인 뒤에 쓴다.
        summarizer = AgentSummarizer(
            AgentClient(self._broker),
            provider=config.capture_provider(),
            model=config.capture_model(),
            work_dir=config.capture_work_dir(),
            timeout_seconds=config.capture_timeout_seconds(),
        )
        route_proposer = RouteProposer(
            AgentClient(self._broker),
            repo_root=config.repo_root(),
            provider=config.capture_provider(),
            model=config.capture_model(),
            work_dir=config.capture_work_dir(),
            timeout_seconds=config.capture_timeout_seconds(),
        )
        # 큐 API 의 `준비 재시도`·`재생성` 이 이 연결을 빌려 쓴다 — 연결을 두 벌 열지 않는다.
        runtime.register(
            summarizer=summarizer,
            route_proposer=route_proposer,
            stages={
                "source_note": SourceNoteStage(
                    AgentClient(self._broker),
                    repo_root=config.repo_root(),
                    provider=config.capture_provider(),
                    model=config.capture_model(),
                    work_dir=config.capture_work_dir(),
                    timeout_seconds=config.capture_timeout_seconds(),
                ),
                "derived": DerivedStage(
                    AgentClient(self._broker),
                    repo_root=config.repo_root(),
                    provider=config.capture_provider(),
                    model=config.capture_model(),
                    work_dir=config.capture_work_dir(),
                    timeout_seconds=config.capture_timeout_seconds(),
                ),
                "concept": ConceptStage(
                    AgentClient(self._broker),
                    repo_root=config.repo_root(),
                    provider=config.capture_provider(),
                    model=config.capture_model(),
                    work_dir=config.capture_work_dir(),
                    timeout_seconds=config.capture_timeout_seconds(),
                ),
                # 잔디의 유일한 게이트. **작성 주체가 여기다** (KDEV-WORK-017 P2).
                "daily": DailyStage(
                    AgentClient(self._broker),
                    repo_root=config.repo_root(),
                    provider=config.capture_provider(),
                    model=config.capture_model(),
                    work_dir=config.capture_work_dir(),
                    timeout_seconds=config.capture_timeout_seconds(),
                ),
            },
            # 잔디의 auto 스테이지 (KDEV-WORK-017 P2). 게이트 실행기와 레지스트리가
            # 다르다 — 계약이 다르고(auto 는 `GateRevision` 을 만들지 않는다) 이름이
            # 겹칠 수도 있다. `collect` 는 LLM 을 부르지 않아 클라이언트가 없다.
            auto_stages={
                # 진짜 git 조사 (KDEV-WORK-017 P5). 계약이 더미와 같아 하류는 그대로다.
                "collect": GitCollect(
                    session_factory=new_session, repo_root=config.repo_root()
                ),
                "investigate": AgentInvestigate(
                    AgentClient(self._broker),
                    provider=config.capture_provider(),
                    model=config.capture_model(),
                    work_dir=config.capture_work_dir(),
                    timeout_seconds=config.capture_timeout_seconds(),
                ),
            },
        )

        # 제출한 실행의 완료를 요청 밖에서 기다렸다가 DB 에 반영한다 (KDEV-WORK-016).
        # 수집도 여기서 한다 — 접수 요청이 15초를 붙잡을 이유가 없다.
        self._driver = PipelineDriver(session_factory=new_session, fetch=fetch_source)
        runtime.register(driver=self._driver)

        runner = QueueIntakeRunner(
            session_factory=new_session,
            sessions=sessions,
            now=lambda: datetime.now(KST),
        )

        bolt_app = await create_capture_app(
            runner,
            sessions,
            bot_token=bot_token,
            allowed_users=config.allowed_slack_users(),
            allowed_channels=config.allowed_slack_channels(),
        )

        self._task = asyncio.create_task(
            self._run_forever(bolt_app, app_token), name="slack-capture"
        )
        # 재시작 전에 진행 중이던 것들을 다시 따라붙는다. 작업은 실행기 큐에 살아 있다.
        await self._driver.recover()
        logger.info("Slack capture started (Socket Mode, in-process)")

    @staticmethod
    async def _run_forever(bolt_app, app_token: str) -> None:
        """웹소켓 루프를 감독한다 — 예외는 back 으로 전파시키지 않고, 끊기면 재기동한다.

        핸들러는 연결 상태를 들고 있으므로 **재기동마다 새로 만든다.** 죽은 핸들러를
        재사용하면 이전 소켓의 잔여 상태를 그대로 물고 들어간다.
        """
        from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

        holder: dict = {}

        async def connect() -> None:
            handler = AsyncSocketModeHandler(bolt_app, app_token)
            holder["handler"] = handler
            await handler.start_async()

        async def close() -> None:
            handler = holder.pop("handler", None)
            closer = getattr(handler, "close_async", None) if handler else None
            if closer is not None:
                await closer()

        async def announce_giveup(message: str) -> None:
            from service.notify import notify_slack

            await notify_slack(f":electric_plug: {message}")

        await supervise_connection(connect, close=close, on_giveup=announce_giveup)

    async def stop(self) -> None:
        # 연결이 닫히면 요약기도 못 쓴다 — 죽은 핸들을 남겨 두면 재시도가 조용히 실패한다.
        runtime.clear()
        if self._driver is not None:
            await self._driver.stop()
            self._driver = None
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except (asyncio.CancelledError, Exception):  # noqa: B014 - 종료 경로에서 삼킨다
                pass
            self._task = None
        if self._redis is not None:
            try:
                await self._redis.aclose()
            except Exception:  # noqa: BLE001
                logger.warning("redis close 실패 (무시)")
            self._redis = None
        if self._broker is not None:
            try:
                await self._broker.close()
            except Exception:  # noqa: BLE001
                logger.warning("broker close 실패 (무시)")
            self._broker = None
