"""접수 이후의 진행 순서 (KDEV-WORK-014 P3).

`prepare` 는 준비만 알고 `open_first_gate` 는 게이트만 안다. 둘을 잇는 "준비가
끝나면 첫 게이트가 열린다"(SPEC-007 S-1 4항)는 **순서에 대한 지식**이라 어느 쪽에도
넣지 않고 여기 둔다. Slack 경로와 큐 API 재시도가 같은 함수를 쓴다.

실행이 비동기가 된 뒤(KDEV-WORK-016)로 그 순서는 **두 시점에 걸쳐** 일어난다.

    start_preparation      수집 + 요약 제출 → `preparing` 으로 두고 즉시 응답
    harvest_preparation    요약 수확 → `in_review` 전이 → 첫 게이트 제출

접수 응답이 준비 완료를 기다리지 않는다는 뜻이다. 화면이 폴링하면서 두 번째를
불러 준다.
"""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import QueueItem

from .definitions import pipeline_for
from .gates import StageRunner, open_first_gate
from .prepare import (
    Fetcher,
    PrepareResult,
    Summarizer,
    completed_auto_stages,
    harvest_auto_stage,
    next_auto_stage,
    running_preparation,
    submit_auto_stage,
)
from .prepare import harvest_preparation as _harvest
from .prepare import submit_preparation

logger = logging.getLogger("kknaks-back.pipeline.flow")


async def start_preparation(
    db: AsyncSession,
    item_id: int,
    *,
    fetch: Fetcher,
    summarize: Summarizer,
) -> PrepareResult:
    """준비를 시작한다 — 수집하고 요약을 제출하는 데까지."""
    return await submit_preparation(db, item_id, fetch=fetch, summarize=summarize)


async def next_auto_runner(
    db: AsyncSession, item: QueueItem, auto_runners: dict[str, Any]
) -> tuple[str | None, Any]:
    """다음에 돌릴 auto 스테이지와 그 실행기. 실행기가 없으면 `(이름, None)`.

    이름은 있는데 실행기가 없다는 것은 **레거시 경로가 그 스테이지를 덮는다**는 뜻이다
    (유튜브의 수집+요약). 없는 것을 있는 척하지 않으려고 이름은 그대로 돌려준다.
    """
    stage = next_auto_stage(
        pipeline_for(item.source_kind), await completed_auto_stages(db, item.id)
    )
    return stage, (auto_runners.get(stage) if stage else None)


async def advance_auto_stages(
    db: AsyncSession,
    item: QueueItem,
    *,
    auto_runners: dict[str, Any],
    runners: dict[str, StageRunner] | None = None,
) -> bool:
    """auto 스테이지 하나를 수확하고 **다음으로 민다.** 더 밀 것이 있으면 `True`.

    준비가 한 번으로 끝나던 시절에는 이 자리가 "수확하면 첫 게이트" 였다. 잔디는
    auto 가 셋이라 그사이에 "다음이 남았나" 가 들어간다 — 남으면 제출하고 `preparing`
    을 유지한 채 돌아가고, 없을 때만 `in_review` 로 넘어가 게이트를 연다.
    """
    preparation = await running_preparation(db, item.id)
    stage_name = str((preparation.payload or {}).get("stage") or "") if preparation else ""
    runner = auto_runners.get(stage_name) if stage_name else None
    if runner is None:
        return False

    result = await harvest_auto_stage(db, item, runner=runner)
    if result.status == "prepare_failed":
        return False
    if result.status != "preparing" or result.preparation_id is None:
        return False
    if (await running_preparation(db, item.id)) is not None:
        # 아직 안 끝났다 — 폴링이 다시 온다.
        return False

    stage, next_runner = await next_auto_runner(db, item, auto_runners)
    if stage is not None and next_runner is not None:
        await submit_auto_stage(db, item.id, stage, runner=next_runner)
        return True

    if stage is not None:
        # 정의에는 남았는데 실행기가 없다. 조용히 게이트로 넘어가면 반쪽짜리 준비가
        # 게이트 입력이 된다 — 그러느니 검토 대기로 두고 사람이 보게 한다.
        logger.warning(
            "auto 스테이지 %s 의 실행기가 없어 준비를 멈춘다 item=%s", stage, item.id
        )
        item.status = "in_review"
        await db.flush()
        return False

    item.status = "in_review"
    await db.flush()

    pipeline = pipeline_for(item.source_kind)
    first_gate = pipeline.first_gate() if pipeline else None
    gate_runner = (runners or {}).get(first_gate.name) if first_gate else None
    if gate_runner is None:
        logger.warning(
            "게이트 제안 경로 미가용 — item=%s 는 게이트 없이 검토 대기 (stage=%s)",
            item.id,
            first_gate.name if first_gate else "(정의 없음)",
        )
        return False
    await open_first_gate(db, item, runner=gate_runner)
    # **아직 밀 것이 남았다.** 게이트는 방금 제출됐을 뿐 내용이 없다(`generating`).
    # 여기서 멈추면 사람이 볼 수 있는 것이 없고, 다음 폴링까지 카드가 빈 채로 있는다.
    # 드라이버가 한 걸음 더 가서 수확하면 그때 `review_pending` 이 된다 — 유튜브
    # 준비부가 `result.ok` 로 `True` 를 돌려주는 것과 같은 이유다.
    return True


async def harvest_preparation(
    db: AsyncSession,
    item: QueueItem,
    *,
    summarize: Summarizer,
    runners: dict[str, StageRunner] | None = None,
) -> PrepareResult:
    """요약을 수확하고, 준비가 끝났으면 첫 게이트를 연다.

    **첫 게이트가 무엇인지는 파이프라인 정의가 정한다** (KDEV-WORK-017 P2). 종전에는
    호출자가 `"route"` 실행기를 집어서 넘겼는데, 그건 유튜브에서만 맞는 이름이었다 —
    잔디의 첫 게이트는 `daily` 다. 이름을 밖에서 박으면 파이프라인이 늘 때마다 호출부가
    같이 틀린다. 그래서 실행기 묶음을 받아 **여기서** 정의를 보고 고른다.

    해당 실행기가 없으면(AI 경로 미가용) 게이트를 열지 않고 `in_review` 로 둔다.
    **준비 결과를 되돌리지는 않는다** — 수집·요약은 이미 끝났고 그건 버릴 이유가
    없다. 게이트는 나중에 열 수 있다.
    """
    result = await _harvest(db, item, summarize=summarize)
    if not result.ok:
        return result

    pipeline = pipeline_for(item.source_kind)
    first_gate = pipeline.first_gate() if pipeline else None
    runner = (runners or {}).get(first_gate.name) if first_gate else None
    if runner is None:
        logger.warning(
            "게이트 제안 경로 미가용 — item=%s 는 게이트 없이 검토 대기 (stage=%s)",
            item.id,
            first_gate.name if first_gate else "(정의 없음)",
        )
        return result

    gate = await open_first_gate(db, item, runner=runner)
    if gate is None:
        # 파이프라인 정의가 없는 종류(블로그·수동 등). 큐에는 남고 화면에 보인다.
        logger.info(
            "파이프라인 정의 없음 — item=%s kind=%s, 게이트 없이 검토 대기",
            item.id,
            item.source_kind,
        )
    return result
