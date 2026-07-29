"""항목 하나를 끝까지 밀어 주는 백그라운드 드라이버 (KDEV-WORK-016 / KDEV-SPEC-009).

**요청은 제출까지만 한다.** 그 뒤를 이어받는 것이 여기다.

    요청 ──[제출]──> 커밋 ──> 응답 (끝)
                       └─ 드라이버: await 실행기 완료 → 수확 → 다음 제출 → …

핵심은 **기다리되 폴링하지 않는다**는 것이다. 실행기는 실행 중 결과 스트림에 이벤트를
흘리고 끝나면 상태를 바꾸며, `AgentClient.result()` 가 그 스트림을 `XREAD BLOCK` 으로
대기하다 깨어난다. 워커가 우리를 깨워 주므로 주기적으로 물어볼 이유가 없다.

드라이버가 죽으면(예외·재시작) 진행이 멈추지만 **잃지는 않는다.** 작업은 실행기 큐에
있고 참조는 DB 에 있다. 두 가지가 복구한다.

    부팅 복구   `recover()` 가 진행 중인 항목을 다시 따라붙는다
    조회 시 수확 화면이 조회하면 그 자리에서 따라잡는다 (`queue.py`)

항목당 태스크는 하나다. 같은 항목을 두 번 따라붙으면 같은 실행을 두 번 수확하려 든다 —
수확 자체가 멱등이라 사고는 안 나지만, 헛돌 이유도 없다.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Awaitable, Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Gate, QueueItem

from . import runtime
from .flow import harvest_preparation, start_preparation
from .gates import IN_FLIGHT, harvest

logger = logging.getLogger("kknaks-back.pipeline.driver")

#: 한 항목을 미는 동안 허용하는 최대 단계 수. 정상 흐름은
#: 준비 → route → source_note → concept → derived 로 열 걸음을 넘지 않는다.
#: 상태 판정이 어긋나 제자리를 도는 경우에 무한 루프가 되지 않게 막는다.
MAX_STEPS = 20


class PipelineDriver:
    """진행 중인 항목을 요청 밖에서 밀어 준다."""

    def __init__(
        self,
        *,
        session_factory: Callable[[], Any],
        fetch: Callable[[str], Awaitable[Any]],
    ) -> None:
        self.session_factory = session_factory
        self.fetch = fetch
        self._tasks: dict[int, asyncio.Task] = {}

    # --- 등록 ---------------------------------------------------------------

    async def follow(self, item_id: int) -> None:
        """이 항목을 이어서 민다. **커밋 뒤에 부른다.**

        커밋 전에 부르면 드라이버가 아직 없는 행을 읽고 할 일이 없다고 판단한다.
        태스크만 만들고 즉시 돌아온다 — 실행 완료를 여기서 기다리지 않는다.
        """
        existing = self._tasks.get(item_id)
        if existing is not None and not existing.done():
            return
        task = asyncio.create_task(self._drive(item_id), name=f"pipeline-item-{item_id}")
        self._tasks[item_id] = task
        task.add_done_callback(lambda t, i=item_id: self._tasks.pop(i, None))

    async def recover(self) -> int:
        """부팅 시 진행 중이던 항목을 다시 따라붙는다.

        드라이버는 프로세스 안에 살아서 재시작에 사라진다. **작업은 사라지지 않는다** —
        실행기 큐에 있고 `external_task_ref` 로 다시 찾는다. 여기서 다시 붙는다.
        """
        async with self.session_factory() as db:
            item_ids = set(
                (
                    await db.scalars(
                        select(QueueItem.id).where(
                            QueueItem.status.in_(("received", "preparing")),
                            QueueItem.deleted_at.is_(None),
                        )
                    )
                ).all()
            )
            item_ids |= set(
                (
                    await db.scalars(
                        select(Gate.item_id)
                        .join(QueueItem, QueueItem.id == Gate.item_id)
                        .where(Gate.status.in_(IN_FLIGHT), QueueItem.deleted_at.is_(None))
                    )
                ).all()
            )

        for item_id in sorted(item_ids):
            await self.follow(item_id)
        if item_ids:
            logger.info("드라이버 복구 — 진행 중 항목 %d건 다시 따라붙음", len(item_ids))
        return len(item_ids)

    async def stop(self) -> None:
        for task in list(self._tasks.values()):
            task.cancel()
        self._tasks.clear()

    # --- 진행 ---------------------------------------------------------------

    async def _drive(self, item_id: int) -> None:
        """더 밀 것이 없을 때까지 한 걸음씩 나아간다."""
        try:
            for _ in range(MAX_STEPS):
                if not await self._step(item_id):
                    return
        except asyncio.CancelledError:
            raise
        except Exception:  # noqa: BLE001 — 드라이버가 죽어도 서비스는 계속된다
            logger.exception("드라이버 중단 item=%s — 조회 시 수확이 따라잡는다", item_id)
            return
        logger.warning("드라이버가 %d 걸음을 넘겼다 item=%s — 멈춘다", MAX_STEPS, item_id)

    async def _step(self, item_id: int) -> bool:
        """한 걸음 민다. 더 밀 것이 있으면 `True`."""
        summarizer = runtime.current_summarizer()
        runners = runtime.current_runners()

        async with self.session_factory() as db:
            item = await db.get(QueueItem, item_id)
            if item is None or item.deleted_at is not None:
                return False

            if item.status == "received":
                if summarizer is None:
                    return False
                return await self._prepare(db, item, summarizer)

            if item.status == "preparing":
                if summarizer is None:
                    return False
                return await self._finish_preparing(db, item, summarizer, runners)

            gate = await db.scalar(
                select(Gate)
                .where(Gate.item_id == item_id, Gate.status.in_(IN_FLIGHT))
                .order_by(Gate.stage_no)
                .limit(1)
            )
            if gate is None:
                # 사람 차례(검토 대기)이거나 끝났다. 드라이버가 할 일은 없다.
                return False
            return await self._finish_gate(db, item, gate, runners)

    async def _prepare(self, db: AsyncSession, item: QueueItem, summarizer) -> bool:
        """수집하고 요약을 제출한다 — **수집도 요청 밖에서** 한다.

        수집은 AI 가 아니지만 최대 15초가 걸린다. 접수 요청 안에서 하면 그만큼
        회신이 늦는다.
        """
        result = await start_preparation(
            db, item.id, fetch=self.fetch, summarize=summarizer
        )
        await db.commit()
        return result.running

    async def _finish_preparing(
        self, db: AsyncSession, item: QueueItem, summarizer, runners
    ) -> bool:
        task_ref = await _running_preparation_ref(db, item.id)
        if task_ref is None:
            # 참조가 없으면 기다릴 대상이 없다. 수확이 실패로 닫는다.
            await harvest_preparation(db, item, summarize=summarizer)
            await db.commit()
            return False

        await summarizer.wait(task_ref)  # ← 워커가 깨워 준다
        result = await harvest_preparation(
            db, item, summarize=summarizer, runner=runners.get("route")
        )
        await db.commit()
        return result.ok

    async def _finish_gate(
        self, db: AsyncSession, item: QueueItem, gate: Gate, runners
    ) -> bool:
        runner = runners.get(gate.stage_name)
        if runner is None:
            return False

        task_ref = await _drafting_task_ref(db, gate.id)
        if task_ref is not None:
            await runner.wait(task_ref)  # ← 워커가 깨워 준다
        await harvest(db, gate, item=item, runner=runner)
        await db.commit()
        # 게이트가 채워지면 **사람 차례**다. 다음 게이트는 승인이 연다 —
        # 드라이버가 더 밀면 사람이 안 본 것을 지나치게 된다.
        return False


async def _running_preparation_ref(db: AsyncSession, item_id: int) -> str | None:
    from core.models import AITask, ItemPreparation

    return await db.scalar(
        select(AITask.external_task_ref)
        .join(ItemPreparation, ItemPreparation.ai_task_id == AITask.id)
        .where(
            ItemPreparation.item_id == item_id,
            ItemPreparation.status == "running",
            AITask.external_task_ref.is_not(None),
        )
        .order_by(ItemPreparation.version.desc())
        .limit(1)
    )


async def _drafting_task_ref(db: AsyncSession, gate_id: int) -> str | None:
    from core.models import AITask, GateRevision

    return await db.scalar(
        select(AITask.external_task_ref)
        .join(GateRevision, GateRevision.ai_task_id == AITask.id)
        .where(
            GateRevision.gate_id == gate_id,
            GateRevision.status == "drafting",
            AITask.external_task_ref.is_not(None),
        )
        .order_by(GateRevision.version.desc())
        .limit(1)
    )
