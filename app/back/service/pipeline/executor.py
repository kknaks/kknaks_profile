"""실행기 호출을 제출과 수확으로 나눈다 (KDEV-WORK-016 P1 / KDEV-SPEC-009 「실행은 비동기다」).

**AI 호출을 사용자 요청 안에서 기다리지 않는다.** 생성은 30~60초가 걸리고, 그동안 요청을
붙잡고 있으면 앞단 프록시가 먼저 끊는다. 그러면 FastAPI 가 요청을 취소하며 트랜잭션이
롤백돼 **승인 자체가 사라진다** — 사용자는 여러 번 눌러도 진행이 안 되는 것만 본다.

open-kknaks 는 이미 Redis 큐다. 그러니 여기서 할 일은 큐를 새로 만드는 것이 아니라
`result()` 로 블로킹하던 것을 **제출 → 폴링 → 수확** 으로 나누는 것뿐이다.

    제출   submit → task_id 를 `ai_tasks.external_task_ref` 에 저장하고 즉시 커밋
    폴링   화면이 게이트를 주기적으로 조회한다
    수확   조회 시 실행 상태를 확인해 끝났으면 결과를 파싱·검증한다

작업은 **실행기의 큐에 남는다.** back 컨테이너가 재시작해도 유실되지 않는다 —
`external_task_ref` 로 다시 찾는다.

스테이지는 무엇을 물어보고(`prompt`·`payload`) 결과를 어떻게 읽는지(`parse`)만 안다.
제출과 폴링 절차는 전부 같으므로 여기 한 번만 둔다.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

#: 아직 끝나지 않은 실행기 상태. `retrying` 은 실행기가 스스로 다시 거는 중이라 실패가 아니다.
RUNNING_STATUSES = ("pending", "running", "retrying")


@dataclass(frozen=True)
class Execution:
    """실행 한 건의 현재 모습. `running` 이면 아직 수확할 것이 없다."""

    status: str  # running · succeeded · failed
    result: str | None = None
    session_ref: str | None = None
    error_code: str | None = None
    error_message: str | None = None

    @property
    def running(self) -> bool:
        return self.status == "running"


RUNNING = Execution(status="running")


def failed(code: str, message: str) -> Execution:
    return Execution(status="failed", error_code=code, error_message=message[:1000])


def _age_seconds(created_at: Any) -> float | None:
    if not isinstance(created_at, datetime):
        return None
    stamp = created_at if created_at.tzinfo else created_at.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - stamp).total_seconds()


def read_execution(task, *, timeout_seconds: float, task_id: str = "") -> Execution:
    """실행기의 Task 하나를 우리 상태로 옮긴다.

    실행기에서 사라진 작업(`None`)은 실패로 본다 — 계속 `running` 으로 두면 게이트가
    영원히 열리지 않고, 사용자는 재시도조차 못 한다.
    """
    if task is None:
        return failed("TASK_NOT_FOUND", f"실행기에 작업 {task_id} 가 없다")

    status = str(getattr(task, "status", "") or "")
    if status in RUNNING_STATUSES:
        age = _age_seconds(getattr(task, "created_at", None))
        if age is not None and age > timeout_seconds:
            # 무한 `generating` 을 막는다. 기록은 남고 화면에는 `재시도` 가 열린다.
            return failed(
                "EXECUTION_TIMEOUT",
                f"{int(age)}초째 끝나지 않았다 (상한 {int(timeout_seconds)}초)",
            )
        return RUNNING

    if status != "done":
        return failed(
            f"EXECUTION_{status.upper() or 'UNKNOWN'}",
            str(getattr(task, "error", None) or f"실행이 {status} 로 끝났다"),
        )

    result = getattr(task, "result", None)
    if not result or not str(result).strip():
        # 빈 결과를 성공으로 넘기면 게이트가 내용 없는 제안을 검토 대기로 연다.
        return failed("EMPTY_RESULT", str(getattr(task, "error", None) or "결과가 비었다"))

    return Execution(
        status="succeeded",
        result=str(result),
        session_ref=getattr(task, "result_session_id", None),
    )


async def await_execution(client, task_id: str, *, timeout_seconds: float) -> Execution:
    """완료를 **기다린다.** 폴링이 아니다.

    실행기는 실행 중 결과 스트림에 이벤트를 흘리고 끝나면 상태를 `done` 으로 바꾼다.
    `AgentClient.result()` 가 그 스트림을 `XREAD BLOCK` 으로 대기하다 깨어난다 —
    **워커가 우리를 깨워 준다.** 그래서 주기적으로 물어볼 이유가 없다.

    이 대기를 요청 안에서 하면 안 된다. 요청 밖(백그라운드 태스크)에서 해야
    프록시가 끊어도 트랜잭션이 롤백되지 않는다.
    """
    return read_execution(
        await client.result(task_id, timeout=timeout_seconds),
        timeout_seconds=timeout_seconds,
        task_id=task_id,
    )


async def poll_execution(client, task_id: str, *, timeout_seconds: float) -> Execution:
    """지금 상태만 본다. **기다리지 않는다.**

    대기는 `await_execution` 이 한다. 이쪽은 화면이 조회할 때 쓰는 안전망이다 —
    대기 태스크가 죽었거나 back 이 재시작한 사이에도 조회 한 번으로 따라잡는다.
    """
    return read_execution(
        await client.broker.get_task(task_id),
        timeout_seconds=timeout_seconds,
        task_id=task_id,
    )


class AgentStage:
    """open-kknaks 에 제출하고 나중에 수확하는 스테이지의 공통부.

    하위 클래스는 세 가지만 채운다.

        prompt(request)  무엇을 시킬 것인가
        payload(request) 무엇을 보고 만들 것인가
        parse(raw, request) 결과를 어떻게 읽고 검증할 것인가

    `parse` 는 **수확 시점에** 불린다. 제출 시점의 지역 변수를 붙잡아 두지 말고
    `request` 에서 다시 읽어야 한다 — back 이 재시작해도 수확이 이어져야 하기 때문이다.
    """

    #: 실행기 metadata 의 `source` 값. 큐에서 어느 스테이지의 작업인지 구분한다.
    source: str = "pipeline"

    def __init__(
        self,
        client,
        *,
        repo_root: Path,
        provider: str,
        model: str | None,
        work_dir: str | None,
        timeout_seconds: float = 900,
    ) -> None:
        self.client = client
        self.repo_root = repo_root
        self.provider = provider
        self.model = model
        self.work_dir = work_dir
        self.timeout_seconds = timeout_seconds

    # --- 스테이지가 채우는 것 -------------------------------------------------

    def prompt(self, request) -> str:
        raise NotImplementedError

    def payload(self, request) -> dict[str, Any]:
        raise NotImplementedError

    def parse(self, raw: str, request) -> dict[str, Any]:
        raise NotImplementedError

    # --- 절차 ---------------------------------------------------------------

    async def submit(self, request) -> str:
        """큐에 넣고 `task_id` 만 받아 돌아온다. 결과를 기다리지 않는다."""
        options: dict[str, Any] = {"cwd": self.work_dir} if self.work_dir else {}
        if request.session_ref:
            # 세션을 이어받으면 원문·지침을 다시 보내지 않아도 된다 (SPEC-009 S-1 5항).
            options["resume"] = {"mode": "session", "session_id": request.session_ref}

        return await self.client.submit(
            self.prompt(request)
            + "\n\n"
            + json.dumps(self.payload(request), ensure_ascii=False),
            provider=self.provider,
            model=self.model,
            options=options or None,
            max_retries=2,
            metadata={"source": self.source, "item_id": request.item.id},
        )

    async def wait(self, task_id: str) -> Execution:
        """완료까지 기다린다 — 백그라운드에서만 부른다."""
        return await await_execution(
            self.client, task_id, timeout_seconds=self.timeout_seconds
        )

    async def poll(self, task_id: str) -> Execution:
        return await poll_execution(
            self.client, task_id, timeout_seconds=self.timeout_seconds
        )
