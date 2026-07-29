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

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import QueueItem

from .gates import StageRunner, open_first_gate
from .prepare import Fetcher, PrepareResult, Summarizer
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


async def harvest_preparation(
    db: AsyncSession,
    item: QueueItem,
    *,
    summarize: Summarizer,
    runner: StageRunner | None = None,
) -> PrepareResult:
    """요약을 수확하고, 준비가 끝났으면 첫 게이트를 연다.

    `runner` 가 없으면(AI 경로 미가용) 게이트를 열지 않고 `in_review` 로 둔다.
    **준비 결과를 되돌리지는 않는다** — 수집·요약은 이미 끝났고 그건 버릴 이유가
    없다. 게이트는 나중에 열 수 있다.
    """
    result = await _harvest(db, item, summarize=summarize)
    if not result.ok:
        return result

    if runner is None:
        logger.warning("게이트 제안 경로 미가용 — item=%s 는 게이트 없이 검토 대기", item.id)
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
