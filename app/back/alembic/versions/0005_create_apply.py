"""create apply plan/result tables (KDEV-WORK-015 Phase 4)

발행 계획과 결과. **성공만 남기지 않는다** — 거부와 실패도 행으로 남아야
"승인했는데 왜 안 나갔지"를 사람이 알 수 있다.

Revision ID: 0005_create_apply
Revises: 0004_fk_set_null
Create Date: 2026-07-28
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0005_create_apply"
down_revision: Union[str, None] = "0004_fk_set_null"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

PLAN_VALIDATION_STATUSES = ("pending", "passed", "rejected")
APPLY_RESULT_STATUSES = ("succeeded", "rejected", "failed")


def _in(column: str, values: tuple[str, ...]) -> str:
    return f"{column} IN ({', '.join(repr(v) for v in values)})"


def upgrade() -> None:
    op.create_table(
        "apply_plans",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("file_actions", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "validation_status", sa.String(length=16), nullable=False, server_default="pending"
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint(
            _in("validation_status", PLAN_VALIDATION_STATUSES),
            name="ck_apply_plans_validation_status",
        ),
        sa.ForeignKeyConstraint(
            ["item_id"], ["queue_items.id"], name="fk_apply_plans_item", ondelete="CASCADE"
        ),
    )
    op.create_index("ix_apply_plans_item_id", "apply_plans", ["item_id"])

    op.create_table(
        "apply_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("plan_id", sa.Integer(), nullable=False),
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("commit_ref", sa.String(length=64)),
        sa.Column("violations", postgresql.JSONB(astext_type=sa.Text())),
        sa.Column("error_code", sa.String(length=64)),
        sa.Column("error_message", sa.Text()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint(_in("status", APPLY_RESULT_STATUSES), name="ck_apply_results_status"),
        sa.ForeignKeyConstraint(
            ["plan_id"], ["apply_plans.id"], name="fk_apply_results_plan", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["item_id"], ["queue_items.id"], name="fk_apply_results_item", ondelete="CASCADE"
        ),
    )
    op.create_index("ix_apply_results_item_id", "apply_results", ["item_id"])


def downgrade() -> None:
    op.drop_index("ix_apply_results_item_id", table_name="apply_results")
    op.drop_table("apply_results")
    op.drop_index("ix_apply_plans_item_id", table_name="apply_plans")
    op.drop_table("apply_plans")
