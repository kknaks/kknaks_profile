"""승인 대기 알림 (KDEV-WORK-017 P5 / KDEV-SPEC-013 U-2).

**알림의 목적이 바뀌었다.** 종전 잔디 잡은 "발행 완료" 를 알렸다 — 이미 레포에 쓰인
뒤라 사람이 할 일이 없는 통지였다. 이제 알릴 것은 **사람이 봐야 하는 것이 생겼다**
는 사실이다. 승인하지 않으면 아무것도 발행되지 않으므로, 이 알림이 안 가면 잔디가
조용히 멈춘다.

두 번 울린다.

    발동 시 1회      게이트가 검토 대기로 열릴 때
    2건 이상 재알림   쌓여 있으면 다시 — 한 번 놓치면 영영 묻히기 때문이다

같은 항목으로 두 번 울리지 않는다. 재알림은 **건수가 늘 때만** 나간다.
"""

from __future__ import annotations

import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import QueueItem
from service.notify import notify_slack

logger = logging.getLogger("kknaks-back.pipeline.review-alert")

#: 이 수를 넘으면 "쌓여 있다" 고 본다. 2건이면 하루를 건너뛴 것이다.
BACKLOG_THRESHOLD = 2


async def pending_count(db: AsyncSession) -> int:
    return int(
        await db.scalar(
            select(func.count())
            .select_from(QueueItem)
            .where(QueueItem.status == "in_review", QueueItem.deleted_at.is_(None))
        )
        or 0
    )


async def notify_review_pending(db: AsyncSession, item: QueueItem) -> bool:
    """게이트가 열렸다는 알림. 보냈으면 `True`.

    **실패해도 파이프라인을 멈추지 않는다** — 알림은 부수 효과이고, Slack 이 죽었다고
    승인 대기 항목이 사라지는 것은 아니다. 대신 로그에 남긴다.
    """
    count = await pending_count(db)
    label = item.source_url or item.note or f"item {item.id}"
    lines = [f":inbox_tray: 승인 대기 — {label}"]
    if count >= BACKLOG_THRESHOLD:
        lines.append(f"*미승인 {count}건이 쌓여 있습니다.* 승인 전에는 아무것도 발행되지 않습니다.")

    try:
        await notify_slack("\n".join(lines))
    except Exception as exc:  # noqa: BLE001
        logger.warning("승인 대기 알림 실패 item=%s: %s", item.id, exc)
        return False
    return True
