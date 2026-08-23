"""입력 접수 — Slack·화면·잡이 같은 큐로 들어온다 (KDEV-WORK-014 P2 / KDEV-SPEC-007).

접수의 계약은 한 줄이다. **이 시점에 레포에는 아무 파일도 생기지 않는다.**

종전에는 Slack 링크 하나가 곧바로 AI 호출 → 파일 쓰기 → `origin/main` 커밋으로 이어졌다.
사람이 끼어들 지점이 없었다. 여기서는 행 하나를 만들고 끝낸다 — 무엇을 만들지는
route 게이트에서 사람이 정한다.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ITEM_PENDING_STATUSES, QueueItem

from .urls import detect_source_kind, normalize_url


@dataclass(frozen=True)
class IntakeResult:
    """접수 결과.

    `outcome` 이 셋인 이유는 **셋의 후속 처리가 다르기** 때문이다.
    - `created` — 자동 준비를 시작한다.
    - `joined` — 이미 준비 중이거나 검토 대기다. 다시 준비하지 않는다.
    - `duplicate_published` — 이미 발행된 자료다. 같은 자료의 재정리가 정당한 경우가
      있으므로 자동으로 막지 않고 **사람에게 물어본다**(SPEC-007 S-4).
    """

    item_id: int | None
    outcome: str  # created · joined · duplicate_published
    existing_item_id: int | None = None

    @property
    def created(self) -> bool:
        return self.outcome == "created"


def _merge_note(existing: str | None, incoming: str | None) -> str | None:
    """합류 시 메모는 **덧붙인다.** 두 번째 투입의 메모가 첫 번째를 덮으면 맥락이 사라진다."""
    if not incoming or not incoming.strip():
        return existing
    incoming = incoming.strip()
    if not existing or not existing.strip():
        return incoming
    if incoming in existing:
        return existing
    return f"{existing}\n\n{incoming}"


async def intake(
    db: AsyncSession,
    *,
    source_url: str | None = None,
    note: str | None = None,
    channel: str = "manual",
    submitted_by: str | None = None,
    source_kind: str | None = None,
    allow_republish: bool = False,
    normalized_key: str | None = None,
) -> IntakeResult:
    """항목을 접수하거나 기존 항목에 합류시킨다.

    `allow_republish=True` 는 "이미 발행된 자료지만 새로 정리하겠다"는 **사람의 결정**이
    내려온 경우다. 기본값이 아니어야 한다 — 기본이면 중복 경고가 무의미해진다.

    `normalized_key` 는 **URL 이 없는 입력의 중복 축**이다 (KDEV-WORK-017 P2). 잔디는
    자료가 아니라 날짜가 항목을 가르므로 `daily:{date}` 를 키로 쓴다. 그러면 아래 중복
    판정이 그대로 날짜 축에서 돌고, `uq_queue_items_pending_url` 부분 유니크 인덱스가
    **마이그레이션 없이** 하루 한 항목을 DB 에서 강제한다. 이미 발행된 날짜를 다시
    접수하면 `duplicate_published` 로 떨어지는데, 그것이 SPEC-013 S-7 3항(사람이
    확인하고 다시 만든다)이 요구하는 동작이다.
    """
    normalized = normalized_key or normalize_url(source_url)
    kind = source_kind or detect_source_kind(source_url)

    if normalized:
        pending = await db.scalar(
            select(QueueItem)
            .where(
                QueueItem.normalized_url == normalized,
                QueueItem.deleted_at.is_(None),
                QueueItem.status.in_(ITEM_PENDING_STATUSES),
            )
            .limit(1)
        )
        if pending is not None:
            merged = _merge_note(pending.note, note)
            if merged != pending.note:
                pending.note = merged
            await db.flush()
            return IntakeResult(
                item_id=pending.id, outcome="joined", existing_item_id=pending.id
            )

        if not allow_republish:
            published = await db.scalar(
                select(QueueItem)
                .where(
                    QueueItem.normalized_url == normalized,
                    QueueItem.deleted_at.is_(None),
                    QueueItem.status == "published",
                )
                .order_by(QueueItem.published_at.desc())
                .limit(1)
            )
            if published is not None:
                return IntakeResult(
                    item_id=None,
                    outcome="duplicate_published",
                    existing_item_id=published.id,
                )

    item = QueueItem(
        source_kind=kind,
        source_url=source_url,
        normalized_url=normalized,
        note=(note or None),
        channel=channel,
        status="received",
        submitted_by=submitted_by,
    )
    db.add(item)
    await db.flush()
    return IntakeResult(item_id=item.id, outcome="created")
