"""활동 0 항목 상태 (KDEV-WORK-017 P5 / KDEV-SPEC-013 §4)

**활동이 없는 날은 실패가 아니다.** 종전에는 `collect` 가 `NO_ACTIVITY` 로 준비를
닫으면서 항목이 `prepare_failed` 로 남았다 — 아무 일도 안 한 날마다 큐에 빨간 줄이
하나씩 쌓인다는 뜻이다.

항목을 아예 만들지 않는 선택지(스펙 원문)는 비용 때문에 못 쓴다. 활동 여부는 조사를
해 봐야 알고, 접수 시점에 한 번 더 조사하면 bare 클론 13개를 하루에 두 번 훑는다.
그렇다고 조사 뒤에 접수하면 "접수는 요청 안에서 조사를 기다리지 않는다"(SPEC-013 §5)와
정면으로 부딪힌다.

그래서 **항목은 남기되 상태로 구분한다.** 지워 버리면 "조사가 돌았는데 활동이 0" 과
"스케줄러가 안 돌았다" 가 구분되지 않는다 — 후자는 고쳐야 할 장애다.

Revision ID: 0008_item_no_activity
Revises: 0007_tracked_repos
Create Date: 2026-08-01
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op

revision: str = "0008_item_no_activity"
down_revision: Union[str, None] = "0007_tracked_repos"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_STATUSES = (
    "received",
    "preparing",
    "in_review",
    "prepare_failed",
    "publishing",
    "published",
    "publish_failed",
    "discarded",
    "deleted",
)
_NEW = (*_STATUSES, "no_activity")


def _values(names: tuple[str, ...]) -> str:
    return ", ".join(f"'{n}'" for n in names)


def upgrade() -> None:
    op.drop_constraint("ck_queue_items_status", "queue_items", type_="check")
    op.create_check_constraint(
        "ck_queue_items_status", "queue_items", f"status IN ({_values(_NEW)})"
    )


def downgrade() -> None:
    # 되돌리기 전에 기존 행을 살려 둔다. 그냥 제약만 좁히면 `no_activity` 행이
    # 남아 있어 마이그레이션이 실패한다.
    op.execute("UPDATE queue_items SET status = 'prepare_failed' WHERE status = 'no_activity'")
    op.drop_constraint("ck_queue_items_status", "queue_items", type_="check")
    op.create_check_constraint(
        "ck_queue_items_status", "queue_items", f"status IN ({_values(_STATUSES)})"
    )
