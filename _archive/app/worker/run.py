"""Example worker — run via docker compose or directly."""

import asyncio
import os

from open_kknaks.broker.redis import RedisBroker
from open_kknaks.config import ClaudeConfig
from open_kknaks.middleware.cost import CostMiddleware
from open_kknaks.middleware.logging import LoggingMiddleware
from open_kknaks.middleware.retries import RetriesMiddleware
from open_kknaks.middleware.timeout import TimeoutMiddleware
from open_kknaks.worker import executor as okk_executor
from open_kknaks.worker.worker import ClaudeWorker

#: 무출력 상한 기본값(초). open-kknaks 기본은 30 이고 그것으로는 잔디가 못 돈다.
DEFAULT_IDLE_TIMEOUT = 180


def apply_idle_timeout(env: dict[str, str] | None = None) -> int:
    """워커의 무출력 상한을 올린다. **open-kknaks 를 고치지 않는다.**

    open-kknaks 는 timeout 을 둘로 나눠 잰다. 전체 데드라인(`options.timeout_sec`)은
    태스크별로 넘길 수 있지만 **무출력 상한은 `executor.IDLE_TIMEOUT` 모듈 상수라
    바깥에서 넘길 자리가 없다.** `ClaudeConfig` 에도 `Task` 에도 없고 env 도 안 읽는다.
    `ClaudeWorker` 가 executor 를 인자로 받지 않고 안에서 만들기 때문에 인스턴스를
    갈아 끼울 수도 없다. 모듈 속성을 부팅 때 덮는 것이 유일한 조정점이다.

    덮어써도 되는 근거는 executor 가 그 상수를 **루프 안에서 매 회전 다시 읽는다**는
    것이다(기본인자 캡처나 `__init__` 복사가 아니다). 부팅 시점 대입이 그대로 먹는다.

    이 값이 필요한 이유는 잔디 파이프라인의 입력이 크기 때문이다. `daily` 게이트는
    investigate 산출물 전량에 템플릿 둘을 얹어 보내는데, 첫 토큰까지 30초를 넘겨
    `IdleTimeoutError` 로 재시도 3회를 소진하고 게이트가 열리지 않았다. `investigate`
    도 실측 25·32초로 같은 벽 바로 앞에 있었다.

    **입자가 워커 전역이라는 것이 이 방식의 한계다** — 태스크별로 다르게 줄 수 없다.
    이 워커가 우리 파이프라인만 돌리므로 지금은 문제가 아니지만, 태스크별 조정이
    필요해지면 open-kknaks 에 `options.idle_timeout_sec` 을 내는 것이 정공법이다.

    Raises:
        RuntimeError: `IDLE_TIMEOUT` 이 사라졌을 때. **조용히 넘어가지 않는다** —
            open-kknaks 를 올렸는데 상수 이름이나 위치가 바뀌면 이 덮어쓰기가 아무
            일도 안 하고 상한이 30초로 되돌아간다. 그 실패는 잔디가 다시 안 도는
            것으로만 드러나서 원인에 닿기까지 오래 걸린다. 부팅에서 소리를 낸다.
    """
    env = os.environ if env is None else env
    if not hasattr(okk_executor, "IDLE_TIMEOUT"):
        raise RuntimeError(
            "open_kknaks.worker.executor.IDLE_TIMEOUT 이 없다 — open-kknaks 가 올라가며 "
            "무출력 상한의 이름이나 위치가 바뀌었다. 이 덮어쓰기를 새 계약에 맞춰 고쳐야 "
            "한다. 그냥 두면 상한이 기본값으로 돌아가 잔디 게이트가 다시 열리지 않는다."
        )

    raw = env.get("IDLE_TIMEOUT_SEC", "")
    try:
        seconds = int(raw) if raw else DEFAULT_IDLE_TIMEOUT
    except ValueError:
        # 오타 하나로 상한이 조용히 바뀌는 것보다 기본값으로 도는 편이 낫다.
        print(f"IDLE_TIMEOUT_SEC 를 읽지 못했다 ({raw!r}) — {DEFAULT_IDLE_TIMEOUT}초로 간다")
        seconds = DEFAULT_IDLE_TIMEOUT

    okk_executor.IDLE_TIMEOUT = seconds
    return seconds


async def main() -> None:
    idle_timeout = apply_idle_timeout()

    broker = RedisBroker(
        url=os.environ.get("REDIS_URL", "redis://localhost:6379"),
        namespace=os.environ.get("NAMESPACE", "example"),
    )
    await broker.connect()

    config = ClaudeConfig(
        work_dir=os.environ.get("WORK_DIR", "/project"),
    )

    worker = ClaudeWorker(
        broker=broker,
        config=config,
        queues=os.environ.get("QUEUES", "default").split(","),
        concurrency=int(os.environ.get("CONCURRENCY", "2")),
        middleware=[
            LoggingMiddleware(),
            RetriesMiddleware(max_retries=2),
            TimeoutMiddleware(),
            CostMiddleware(
                worker_budget_usd=5.0,
                global_budget_usd=20.0,
            ),
        ],
    )

    print(
        f"Worker starting: queues={worker.queues}, concurrency={worker.concurrency}, "
        f"idle_timeout={idle_timeout}s"
    )

    try:
        await worker.run()
    finally:
        await broker.close()


if __name__ == "__main__":
    asyncio.run(main())
