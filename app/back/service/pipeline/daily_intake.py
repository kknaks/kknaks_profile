"""잔디 접수 진입점 (KDEV-WORK-017 P2 / KDEV-SPEC-013).

**접수는 행 하나를 만들고 끝난다.** 조사도 AI 호출도 여기서 하지 않는다 — 드라이버가
이어서 민다. P2 에서는 사람이 큐 API 로 부르고, P5 에서 스케줄러가 같은 함수를 부른다.

날짜가 항목을 가른다. 자료를 정리하는 유튜브와 달리 잔디는 **하루가 단위**라, 중복
판정 축이 URL 이 아니라 날짜다. `normalized_url` 에 `daily:{date}` 합성 키를 넣어
기존 중복 판정을 그대로 쓴다 — 컬럼도 인덱스도 늘리지 않는다.

접수 전에 막는 것이 둘이다. 둘 다 **만들지 않는 것이 옳은** 경우라 항목을 만들고
실패시키지 않는다.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date as date_cls
from datetime import datetime, timedelta, timezone
from pathlib import Path

import frontmatter
from sqlalchemy.ext.asyncio import AsyncSession

import config
from service.notify import notify_slack

from .intake import IntakeResult, intake

logger = logging.getLogger("kknaks-back.pipeline.daily-intake")

KST = timezone(timedelta(hours=9))

#: 합성 키 접두. `collect` 가 대상 날짜를 여기서 읽는다.
KEY_PREFIX = "daily:"


@dataclass(frozen=True)
class DailyIntakeResult:
    """접수 결과.

    `blocked` 가 따로 있는 이유는 **실패가 아니기** 때문이다. 본인이 쓴 날은 만들지
    않는 것이 정상 동작이고, 미래 날짜는 사람의 오타다. 둘 다 재시도할 것이 없다.
    """

    outcome: str  # created · joined · duplicate_published · blocked
    date: str
    item_id: int | None = None
    existing_item_id: int | None = None
    reason: str | None = None

    @property
    def created(self) -> bool:
        return self.outcome == "created"


def default_target(now: datetime | None = None) -> date_cls:
    """대상 날짜 기본값 — **어제(KST)**.

    잡이 09:05 KST 에 도는 것을 전제한 값이다. 그 시각의 "어제" 가 방금 끝난 하루다.
    """
    return ((now or datetime.now(KST)).astimezone(KST).date()) - timedelta(days=1)


def synthetic_key(target: date_cls) -> str:
    return f"{KEY_PREFIX}{target.isoformat()}"


def user_authored(repo_root: Path, target: date_cls) -> bool:
    """그날 daily 를 **사람이 직접 썼는가.**

    `auto: true` 가 아니면 사람 것으로 본다 — 키가 없는 옛 파일도 사람 소유다.
    자동 생성분만 명시적으로 표시되므로 이쪽이 안전한 기본값이다.
    """
    path = repo_root / "persona" / "daily" / f"{target.isoformat()}.md"
    if not path.exists():
        return False
    try:
        meta = frontmatter.load(path).metadata
    except Exception:  # noqa: BLE001 — 읽을 수 없으면 건드리지 않는 편이 안전하다
        logger.warning("daily/%s.md 를 읽지 못했다 — 사람 작성으로 본다", target)
        return True
    return meta.get("auto") is not True


async def intake_daily(
    db: AsyncSession,
    *,
    repo_root: Path,
    target: date_cls | None = None,
    note: str | None = None,
    channel: str = "scheduler",
    submitted_by: str | None = None,
    allow_republish: bool = False,
    now: datetime | None = None,
) -> DailyIntakeResult:
    """그날 잔디 항목을 접수한다. 날짜를 지정하면 백필이다.

    막는 것 둘.

        미래 날짜        아직 오지 않은 하루를 조사할 수 없다. 사람의 오타다
        본인 작성        `auto: true` 가 아닌 daily 가 이미 있다 (SPEC-012 S-5)

    **활동 0은 여기서 막지 않는다.** 활동 여부는 조사를 해 봐야 알고, 조사는 `collect`
    스테이지의 일이다. 접수 시점에 한 번 더 조사하면 bare 클론 13개를 하루에 두 번
    훑는다. `collect` 가 `NO_ACTIVITY` 로 준비를 닫고 항목은 `no_activity` 로 종결된다
    — 실패가 아니라 정상 결과이고, 큐 기본 목록에서는 감춰진다(SPEC-013 v0.0.3 §4).
    """
    target = target or default_target(now)
    today = (now or datetime.now(KST)).astimezone(KST).date()
    if target > today:
        return DailyIntakeResult(
            outcome="blocked", date=target.isoformat(), reason="FUTURE_DATE"
        )

    if user_authored(repo_root, target):
        logger.info("daily/%s.md 가 본인 작성 — 접수하지 않는다", target)
        return DailyIntakeResult(
            outcome="blocked", date=target.isoformat(), reason="USER_AUTHORED_DAILY"
        )

    result: IntakeResult = await intake(
        db,
        note=note,
        channel=channel,
        submitted_by=submitted_by,
        source_kind="daily_commit",
        allow_republish=allow_republish,
        normalized_key=synthetic_key(target),
    )
    return DailyIntakeResult(
        outcome=result.outcome,
        date=target.isoformat(),
        item_id=result.item_id,
        existing_item_id=result.existing_item_id,
    )


async def run_daily_intake_job(target: date_cls | None = None) -> dict:
    """스케줄러가 부르는 잔디 잡 — **접수만 한다** (KDEV-WORK-017 P5).

    종전 `run_daily_activity_job` 은 조사·요약·파일 쓰기·push 를 잡 안에서 다 했다.
    이제 잡이 하는 일은 큐에 항목 하나를 넣는 것뿐이고, 조사도 작성도 발행도
    **드라이버와 게이트**가 이어받는다 — 사람의 승인 없이 레포에 쓰이는 경로를
    없애는 것이 이 발주의 목적이다.

    `target` 을 주면 백필이다. 스케줄러는 안 주고 어제로 떨어진다.

    예외를 삼키지 않는다 — 접수가 실패하면 그날 잔디가 통째로 없다. 다만 알림은
    보내고 다시 던진다(APScheduler 가 로그에 남긴다).
    """
    from core.db import new_session

    try:
        async with new_session() as db:
            result = await intake_daily(db, repo_root=config.repo_root(), target=target)
            await db.commit()
    except Exception as exc:  # noqa: BLE001
        await notify_slack(
            f":x: 잔디 접수 실패 — `{type(exc).__name__}: {str(exc)[:300]}`"
        )
        raise

    logger.info("잔디 접수 — %s (%s)", result.date, result.outcome)
    return {
        "date": result.date,
        "outcome": result.outcome,
        "item_id": result.item_id,
        "reason": result.reason,
    }
