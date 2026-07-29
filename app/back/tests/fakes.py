"""테스트용 스테이지 실행기 (KDEV-WORK-016 P1).

실행이 비동기가 된 뒤로 게이트는 **제출과 수확 두 단계**를 거친다. 테스트도 그 두 단계를
그대로 밟아야 실제 흐름을 검증한다 — 한 번에 끝나는 가짜를 쓰면 "폴링 전에는 내용이 없다"는
계약이 검증되지 않는다.

    gate = await open_first_gate(db, item, runner=runner)   # 제출 — drafting
    await harvest(db, gate, item=item, runner=runner)       # 수확 — reviewable
"""

from __future__ import annotations

from typing import Any

from core.models import Gate, QueueItem
from service.pipeline.executor import Execution
from service.pipeline.gates import harvest


class FakeRunner:
    """`StageRunner` 를 흉내 낸다. 실행기 큐 대신 메모리에서 답한다."""

    def __init__(
        self,
        *,
        payload: dict[str, Any] | None = None,
        session_ref: str | None = "sess-1",
        fail_times: int = 0,
        pending: bool = False,
        raw: str = "{}",
    ) -> None:
        self.payload = payload if payload is not None else {}
        self.session_ref = session_ref
        #: 이 횟수만큼 실행이 실패한다 — 재시도 경로를 만든다.
        self.fail_times = fail_times
        #: True 면 폴링이 계속 `running` — 아직 안 끝난 실행을 흉내 낸다.
        self.pending = pending
        self.raw = raw
        #: `submit` 이 받은 request 들. 세션 resume·피드백 전달을 여기서 확인한다.
        self.calls: list = []
        #: `parse` 가 받은 request 들 — 수확 시점의 입력이 제대로 재조립되는지 본다.
        self.parsed: list = []
        self.polled: list[str] = []
        self._issued = 0

    async def submit(self, request) -> str:
        self.calls.append(request)
        self._issued += 1
        return f"task-{self._issued}"

    async def poll(self, task_id: str) -> Execution:
        self.polled.append(task_id)
        if self.pending:
            return Execution(status="running")
        if self.fail_times > 0:
            self.fail_times -= 1
            return Execution(
                status="failed",
                error_code="RuntimeError",
                error_message="provider timeout",
            )
        return Execution(status="succeeded", result=self.raw, session_ref=self.session_ref)

    def parse(self, raw: str, request) -> dict[str, Any]:
        self.parsed.append(request)
        return self.payload


async def collect(db, gate: Gate, *, item: QueueItem, runner) -> bool:
    """화면 폴링 한 번에 해당한다 — 제출해 둔 실행을 수확한다."""
    return await harvest(db, gate, item=item, runner=runner)
