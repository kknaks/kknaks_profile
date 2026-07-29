"""준비에 진행 중 상태를 더한다 (KDEV-WORK-016 Phase 2)

요약 호출이 제출/수확으로 갈리면서 준비도 **끝나지 않은 상태**를 가진다.
게이트 버전의 `drafting` 과 같은 자리다 — 수집 결과는 이미 저장됐지만
요약이 아직 실행기 큐에 있는 구간.

이 행이 있어야 back 이 재시작해도 수확할 재료(수집 원문·메모)가 남는다.
`running` 없이 성공했을 때만 행을 만들면 그 사이의 재료를 어디에도 둘 수 없다.

Revision ID: 0006_preparation_running
Revises: 0005_create_apply
Create Date: 2026-07-29
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op

revision: str = "0006_preparation_running"
down_revision: Union[str, None] = "0005_create_apply"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

CONSTRAINT = "ck_item_preparations_status"
TABLE = "item_preparations"

BEFORE = ("succeeded", "failed")
AFTER = ("running", "succeeded", "failed")


def _in(column: str, values: tuple[str, ...]) -> str:
    return f"{column} IN ({', '.join(repr(v) for v in values)})"


def upgrade() -> None:
    op.drop_constraint(CONSTRAINT, TABLE, type_="check")
    op.create_check_constraint(CONSTRAINT, TABLE, _in("status", AFTER))


def downgrade() -> None:
    # 진행 중이던 준비는 되돌릴 자리가 없다. 지우지 않고 실패로 닫는다 —
    # 무엇이 돌고 있었는지는 payload 와 ai_task 에 남는다.
    op.execute(f"UPDATE {TABLE} SET status = 'failed' WHERE status = 'running'")
    op.drop_constraint(CONSTRAINT, TABLE, type_="check")
    op.create_check_constraint(CONSTRAINT, TABLE, _in("status", BEFORE))
