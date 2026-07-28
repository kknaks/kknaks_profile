"""체인 진행 — 승인이 다음 게이트를 연다 (KDEV-WORK-015 / KDEV-SPEC-008).

**체인 길이는 route 승인이 확정한다.** route 에서 끈 산출물의 스테이지는 아예
생성되지 않는다. 그래서 "다음 스테이지"는 파이프라인 정의만으로 정해지지 않고
**route 결과를 함께 봐야** 한다.

중간 게이트 승인은 다음 스테이지를 열 뿐 파일을 만들지 않는다.
**마지막 게이트 승인이 발행 트리거**다(KDEV-DEC-011 D6).
"""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Gate, GateRevision, QueueItem

from .definitions import pipeline_for
from .gates import Generator, approved_route_payload, open_gate

logger = logging.getLogger("kknaks-back.pipeline.chain")

#: 목적지 키 → 그 목적지를 만드는 스테이지.
DESTINATION_STAGE = {
    "reference": "source_note",
    "concept": "concept",
    "derived": "derived",
}


def enabled_stages(route_payload: dict[str, Any] | None) -> tuple[str, ...]:
    """route 결과가 켠 게이트 스테이지들 — 파이프라인 정의 순서를 따른다.

    `exclusive`(보류·폐기)면 뒤 게이트가 하나도 없다. 만들 것이 없으니
    검토할 것도 없다 — 보류는 route 승인만으로 발행 대상이 된다.
    """
    if not route_payload or route_payload.get("exclusive"):
        return ()
    destinations = route_payload.get("destinations") or {}
    return tuple(
        stage
        for key, stage in DESTINATION_STAGE.items()
        if (destinations.get(key) or {}).get("enabled")
    )


def next_stage(
    source_kind: str, route_payload: dict[str, Any] | None, *, after: str
) -> str | None:
    """`after` 스테이지 다음에 열려야 할 게이트. 없으면 `None`(= 발행 차례)."""
    pipeline = pipeline_for(source_kind)
    if pipeline is None:
        return None

    order = [s.name for s in pipeline.gate_stages()]
    enabled = set(enabled_stages(route_payload))
    try:
        start = order.index(after) + 1
    except ValueError:
        return None
    for name in order[start:]:
        if name in enabled:
            return name
    return None


async def reopen_route(
    db: AsyncSession, item: QueueItem, *, generator: Generator
) -> Gate:
    """목적지 재검토 — **유일한 역방향 전이**다 (KDEV-DEC-011 D5 / SPEC-008 U-6).

    route 가 체인 길이를 정하므로, 목적지를 잘못 고르면 뒤가 전부 헛돈다. 그래서
    여기만 되돌릴 수 있다.

    되돌리는 것과 남기는 것을 구분한다.
    - **되돌린다**: 승인 포인터, 뒤 게이트의 유효성
    - **남긴다**: 모든 revision 내용, 실행 이력, 피드백. 기록은 불변이다.

    **자동 준비 산출물은 재사용한다** — 수집·요약을 다시 돌리지 않는다. 목적지 판단이
    틀린 것이지 원문이 바뀐 게 아니다.
    """
    from sqlalchemy import select

    from .gates import GateError, _generate

    gate = await db.scalar(
        select(Gate)
        .where(Gate.item_id == item.id, Gate.stage_name == "route", Gate.status != "cancelled")
        .limit(1)
    )
    if gate is None:
        raise GateError("GATE_NOT_FOUND", "재오픈할 route 게이트가 없다")
    if item.status in ("publishing", "published"):
        # 이미 나간 것을 되돌리는 것은 제품 기능이 아니다(DEC-012 D7).
        raise GateError(
            "REOPEN_NOT_ALLOWED", f"항목이 {item.status} 라 목적지를 되돌릴 수 없다"
        )

    if gate.approved_revision_id is not None:
        approved = await db.get(GateRevision, gate.approved_revision_id)
        if approved is not None:
            # 내용은 그대로 두고 상태만 밀어낸다 — 무엇을 승인했었는지가 남아야 한다.
            approved.status = "superseded"
        gate.approved_revision_id = None

    # 뒤 게이트는 전제가 사라졌으므로 무효화한다. 지우지 않는다.
    later = (
        await db.scalars(
            select(Gate).where(
                Gate.item_id == item.id,
                Gate.stage_name != "route",
                Gate.status != "cancelled",
            )
        )
    ).all()
    for downstream in later:
        downstream.status = "cancelled"

    if item.status == "discarded":
        # 폐기했던 항목을 되살리는 경로이기도 하다.
        item.status = "in_review"

    gate.status = "regenerating"
    await db.flush()
    await _generate(db, gate, item=item, generator=generator)
    return gate


async def advance(
    db: AsyncSession,
    item: QueueItem,
    gate: Gate,
    *,
    generators: dict[str, Generator],
) -> Gate | None:
    """방금 승인된 게이트 뒤를 잇는다.

    다음 스테이지가 있으면 그 게이트를 열고, 없으면 `None` 을 돌려준다 —
    호출자가 그것을 **발행 신호**로 읽는다.
    """
    # 방금 승인된 것이 route 게이트라도 여기서 찾힌다 — `approve()` 가 같은 세션에서
    # 상태와 승인 포인터를 이미 채웠기 때문이다.
    route_payload = await approved_route_payload(db, item.id)
    stage = next_stage(item.source_kind, route_payload, after=gate.stage_name)
    if stage is None:
        return None

    generator = generators.get(stage)
    if generator is None:
        # 없는 것을 있는 척하지 않는다. 게이트를 열어 두면 사람이 승인할 수 없는
        # 카드가 화면에 남는다.
        logger.warning("스테이지 %s 의 생성기가 없어 게이트를 열지 않는다 item=%s", stage, item.id)
        return None
    return await open_gate(db, item, stage, generator=generator)
