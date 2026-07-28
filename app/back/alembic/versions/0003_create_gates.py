"""create gate chain tables (KDEV-WORK-014 Phase 1)

gates · gate_revisions · gate_feedbacks.

세 테이블은 서로를 가리켜 **순환 FK** 가 된다
(`gates.active_revision_id → gate_revisions`, `gate_revisions.gate_id → gates`,
 `gate_revisions.feedback_id → gate_feedbacks`, `gate_feedbacks.target_revision_id → gate_revisions`).
그래서 테이블을 먼저 만들고 앞을 가리키는 FK 는 `create_foreign_key` 로 뒤에 붙인다.

Revision ID: 0003_create_gates
Revises: 0002_create_queue
Create Date: 2026-07-28
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0003_create_gates"
down_revision: Union[str, None] = "0002_create_queue"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

GATE_STATUSES = (
    "not_started",
    "generating",
    "review_pending",
    "failed",
    "feedback_pending",
    "regenerating",
    "approved",
    "cancelled",
)
REVISION_STATUSES = ("drafting", "reviewable", "approved", "superseded", "failed")
FEEDBACK_STATUSES = ("submitted", "consumed")


def _in(column: str, values: tuple[str, ...]) -> str:
    joined = ", ".join(f"'{v}'" for v in values)
    return f"{column} IN ({joined})"


def _now() -> sa.sql.elements.ColumnElement:
    return sa.func.now()


def upgrade() -> None:
    op.create_table(
        "gates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("stage_name", sa.String(length=32), nullable=False),
        sa.Column("stage_no", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="not_started"),
        sa.Column("active_revision_id", sa.Integer()),
        sa.Column("approved_revision_id", sa.Integer()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=_now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=_now(), nullable=False
        ),
        sa.CheckConstraint(_in("status", GATE_STATUSES), name="ck_gates_status"),
        sa.ForeignKeyConstraint(
            ["item_id"], ["queue_items.id"], name="fk_gates_item", ondelete="CASCADE"
        ),
    )
    # 항목·스테이지당 살아 있는 게이트는 하나.
    # route 재오픈으로 무효화된 `cancelled` 게이트는 이력이라 제약에서 뺀다.
    op.create_index(
        "uq_gates_live_stage",
        "gates",
        ["item_id", "stage_name"],
        unique=True,
        postgresql_where=sa.text("status <> 'cancelled'"),
    )

    op.create_table(
        "gate_revisions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("gate_id", sa.Integer(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="drafting"),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text())),
        sa.Column("parent_revision_id", sa.Integer()),
        sa.Column("feedback_id", sa.Integer()),
        sa.Column("ai_task_id", sa.Integer()),
        sa.Column("session_ref", sa.String(length=128)),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=_now(), nullable=False
        ),
        sa.CheckConstraint(_in("status", REVISION_STATUSES), name="ck_gate_revisions_status"),
        sa.ForeignKeyConstraint(
            ["gate_id"], ["gates.id"], name="fk_gate_revisions_gate", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["parent_revision_id"], ["gate_revisions.id"], name="fk_gate_revisions_parent"
        ),
        sa.ForeignKeyConstraint(
            ["ai_task_id"], ["ai_tasks.id"], name="fk_gate_revisions_ai_task"
        ),
    )
    op.create_index(
        "uq_gate_revisions_version", "gate_revisions", ["gate_id", "version"], unique=True
    )
    # 게이트당 승인 버전은 하나 — DB 가 강제한다.
    # ("검토 가능 버전 하나" 는 전이 순간의 경합 때문에 앱 sweep 소관 — SPEC-009 §5)
    op.create_index(
        "uq_gate_revisions_approved",
        "gate_revisions",
        ["gate_id"],
        unique=True,
        postgresql_where=sa.text("status = 'approved'"),
    )

    op.create_table(
        "gate_feedbacks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("gate_id", sa.Integer(), nullable=False),
        sa.Column("target_revision_id", sa.Integer()),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="submitted"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=_now(), nullable=False
        ),
        sa.CheckConstraint(_in("status", FEEDBACK_STATUSES), name="ck_gate_feedbacks_status"),
        sa.ForeignKeyConstraint(
            ["gate_id"], ["gates.id"], name="fk_gate_feedbacks_gate", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["target_revision_id"],
            ["gate_revisions.id"],
            name="fk_gate_feedbacks_target_revision",
        ),
    )
    op.create_index("ix_gate_feedbacks_gate_id", "gate_feedbacks", ["gate_id"])

    # 순환 FK — 대상 테이블이 생긴 뒤에 붙인다.
    op.create_foreign_key(
        "fk_gates_active_revision", "gates", "gate_revisions", ["active_revision_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_gates_approved_revision", "gates", "gate_revisions", ["approved_revision_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_gate_revisions_feedback",
        "gate_revisions",
        "gate_feedbacks",
        ["feedback_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_gate_revisions_feedback", "gate_revisions", type_="foreignkey")
    op.drop_constraint("fk_gates_approved_revision", "gates", type_="foreignkey")
    op.drop_constraint("fk_gates_active_revision", "gates", type_="foreignkey")
    op.drop_index("ix_gate_feedbacks_gate_id", table_name="gate_feedbacks")
    op.drop_table("gate_feedbacks")
    op.drop_index("uq_gate_revisions_approved", table_name="gate_revisions")
    op.drop_index("uq_gate_revisions_version", table_name="gate_revisions")
    op.drop_table("gate_revisions")
    op.drop_index("uq_gates_live_stage", table_name="gates")
    op.drop_table("gates")
