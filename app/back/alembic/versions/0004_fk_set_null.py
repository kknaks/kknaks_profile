"""nullable FK 를 ON DELETE SET NULL 로 (KDEV-WORK-014 P3)

항목을 hard delete 하면 `queue_items` → `ai_tasks`·`gates` → `gate_revisions` 가
CASCADE 로 지워진다. 그런데 **참조가 그 사이를 가로지른다** —
`gate_revisions.ai_task_id → ai_tasks`, `gates.active_revision_id → gate_revisions`
같은 것들이다. 삭제 순서가 맞지 않는 순간 FK 위반이 나고 삭제 전체가 실패한다.

    ForeignKeyViolation: update or delete on table "ai_tasks" violates
    foreign key constraint "fk_gate_revisions_ai_task" on table "gate_revisions"

소유 관계(`item_id`·`gate_id`)는 CASCADE 그대로 두고, **가로지르는 nullable 참조만**
SET NULL 로 바꾼다. CASCADE 로 두면 실행 행 하나가 지워질 때 그걸 참조하던 제안
버전까지 사라져, 이력 테이블이 불변이라는 전제가 깨진다.

운영 경로는 soft delete 라 이 상황이 자주 오지는 않는다. 다만 "지울 수 있는 구조"를
검증하는 테스트가 있고, 그게 통과하려면 삭제가 실제로 성립해야 한다.

Revision ID: 0004_fk_set_null
Revises: 0003_create_gates
Create Date: 2026-07-28
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op

revision: str = "0004_fk_set_null"
down_revision: Union[str, None] = "0003_create_gates"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# (제약명, 테이블, 컬럼, 참조 테이블)
CROSSING_FKS = [
    ("fk_ai_tasks_retry_of", "ai_tasks", "retry_of_task_id", "ai_tasks"),
    ("fk_item_preparations_ai_task", "item_preparations", "ai_task_id", "ai_tasks"),
    ("fk_gates_active_revision", "gates", "active_revision_id", "gate_revisions"),
    ("fk_gates_approved_revision", "gates", "approved_revision_id", "gate_revisions"),
    ("fk_gate_revisions_parent", "gate_revisions", "parent_revision_id", "gate_revisions"),
    ("fk_gate_revisions_ai_task", "gate_revisions", "ai_task_id", "ai_tasks"),
    ("fk_gate_revisions_feedback", "gate_revisions", "feedback_id", "gate_feedbacks"),
    (
        "fk_gate_feedbacks_target_revision",
        "gate_feedbacks",
        "target_revision_id",
        "gate_revisions",
    ),
]


def _recreate(ondelete: str | None) -> None:
    for name, table, column, target in CROSSING_FKS:
        op.drop_constraint(name, table, type_="foreignkey")
        op.create_foreign_key(name, table, target, [column], ["id"], ondelete=ondelete)


def upgrade() -> None:
    _recreate("SET NULL")


def downgrade() -> None:
    _recreate(None)
