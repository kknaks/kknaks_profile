"""접수 이후의 진행 순서 (KDEV-WORK-014 P3).

`prepare_item` 은 준비만 알고 `open_first_gate` 는 게이트만 안다. 둘을 잇는 "준비가
끝나면 첫 게이트가 열린다"(SPEC-007 S-1 4항)는 **순서에 대한 지식**이라 어느 쪽에도
넣지 않고 여기 둔다. Slack 경로와 큐 API 재시도가 같은 함수를 쓴다.
"""

from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import QueueItem

from .gates import StageRunner, open_first_gate
from .prepare import Fetcher, PrepareResult, Summarizer, prepare_item

logger = logging.getLogger("kknaks-back.pipeline.flow")


async def prepare_and_open_gate(
    db: AsyncSession,
    item_id: int,
    *,
    fetch: Fetcher,
    summarize: Summarizer,
    runner: StageRunner | None = None,
) -> PrepareResult:
    """준비하고, 성공하면 첫 게이트를 연다.

    `runner` 가 없으면(AI 경로 미가용) 게이트를 열지 않고 `in_review` 로 둔다.
    **준비 결과를 되돌리지는 않는다** — 수집·요약은 이미 끝났고 그건 버릴 이유가 없다.
    게이트는 나중에 열 수 있다.
    """
    result = await prepare_item(db, item_id, fetch=fetch, summarize=summarize)
    if not result.ok or runner is None:
        if result.ok:
            logger.warning("게이트 제안 경로 미가용 — item=%s 는 게이트 없이 검토 대기", item_id)
        return result

    item = await db.get(QueueItem, item_id)
    if item is not None:
        gate = await open_first_gate(db, item, runner=runner)
        if gate is None:
            # 파이프라인 정의가 없는 종류(블로그·수동 등). 큐에는 남고 화면에 보인다.
            logger.info(
                "파이프라인 정의 없음 — item=%s kind=%s, 게이트 없이 검토 대기",
                item_id,
                item.source_kind,
            )
    return result
