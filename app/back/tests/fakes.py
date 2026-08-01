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
from service.pipeline import harvest_preparation, start_preparation
from service.pipeline.driver import PipelineDriver
from service.pipeline.executor import Execution
from service.pipeline.gates import harvest
from service.pipeline.prepare import PrepareResult


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

    async def wait(self, task_id: str) -> Execution:
        """가짜는 즉시 답한다 — 실물은 실행기 스트림이 깨워 준다."""
        return await self.poll(task_id)

    def parse(self, raw: str, request) -> dict[str, Any]:
        self.parsed.append(request)
        return self.payload


async def collect(db, gate: Gate, *, item: QueueItem, runner) -> bool:
    """화면 폴링 한 번에 해당한다 — 제출해 둔 실행을 수확한다."""
    return await harvest(db, gate, item=item, runner=runner)


class FakeSummarizer:
    """요약 실행기를 흉내 낸다 (KDEV-WORK-016 P2).

    `on_submit` 은 실제 요약기가 제출 시점에 하는 일(프롬프트 직렬화 등)을
    끼워 넣는 자리다 — 가짜가 그걸 건너뛰면 운영에서만 터지는 결함이 남는다.
    """

    def __init__(
        self,
        *,
        summary: str = "요약본",
        session_ref: str | None = "sess-1",
        fail_times: int = 0,
        pending: bool = False,
        on_submit=None,
    ) -> None:
        self.summary = summary
        self.session_ref = session_ref
        self.fail_times = fail_times
        self.pending = pending
        self.on_submit = on_submit
        #: `submit` 이 받은 `(material, note)` 들.
        self.calls: list[tuple[Any, str | None]] = []
        self.polled: list[str] = []
        self._issued = 0

    async def submit(self, *, material: Any, note: str | None) -> str:
        self.calls.append((material, note))
        if self.on_submit is not None:
            self.on_submit(material=material, note=note)
        self._issued += 1
        return f"sum-{self._issued}"

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
        return Execution(
            status="succeeded", result=self.summary, session_ref=self.session_ref
        )

    async def wait(self, task_id: str) -> Execution:
        return await self.poll(task_id)

    def parse(self, raw: str) -> str:
        summary = (raw or "").strip()
        if not summary:
            raise RuntimeError("open_kknaks returned no summary")
        return summary


class InlineDriver(PipelineDriver):
    """드라이버를 **그 자리에서** 돌린다.

    실 드라이버는 백그라운드 태스크를 만들고 돌아가므로, 테스트가 결과를 보려면
    태스크가 끝나기를 기다려야 한다 — 그건 타이밍에 기대는 테스트가 된다.
    가짜 실행기는 즉시 답하므로 인라인으로 돌려도 같은 경로를 그대로 태운다.
    """

    async def follow(self, item_id: int) -> None:
        await self._drive(item_id)


def first_gate_runners(item: QueueItem, runner) -> dict[str, Any]:
    """실행기 하나를 **그 항목의 첫 게이트 이름**에 걸어 준다.

    수확부가 실행기를 이름으로 찾게 된 뒤로(WORK-017 P2) 필요해진 번역이다.
    테스트는 여전히 "이 게이트 실행기 하나" 만 신경 쓰면 되고, 이름이 유튜브면
    `route`·잔디면 `daily` 라는 사실은 정의에서 나온다.
    """
    from service.pipeline.definitions import pipeline_for

    pipeline = pipeline_for(item.source_kind)
    stage = pipeline.first_gate() if pipeline else None
    return {stage.name: runner} if stage and runner is not None else {}


async def prepare(db, item_id: int, *, fetch, summarize, runner=None) -> PrepareResult:
    """준비를 제출하고 곧바로 수확한다 — 종전의 동기 `prepare_item` 한 번에 해당한다.

    제출과 수확 사이를 벌려 보고 싶은 테스트는 이 헬퍼를 쓰지 않고 두 함수를
    직접 부른다.
    """
    result = await start_preparation(db, item_id, fetch=fetch, summarize=summarize)
    if not result.running:
        return result
    item = await db.get(QueueItem, item_id)
    return await harvest_preparation(
        db, item, summarize=summarize, runners=first_gate_runners(item, runner)
    )
