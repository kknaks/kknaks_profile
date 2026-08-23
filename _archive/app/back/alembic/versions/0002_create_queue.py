"""create approval queue tables (KDEV-WORK-014 Phase 1)

queue_items · ai_tasks · item_preparations.

`users` 는 건드리지 않는다 — 파이프라인 테이블과 FK 로 잇지 않는 설계다
(단일 관리자라 소유자 구분이 불필요하고, `submitted_by` 는 Slack 사용자
식별자를 담을 수 있어 문자열이다).

Revision ID: 0002_create_queue
Revises: 0001_create_users
Create Date: 2026-07-28
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0002_create_queue"
down_revision: Union[str, None] = "0001_create_users"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ITEM_STATUSES = (
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
ITEM_PENDING_STATUSES = (
    "received",
    "preparing",
    "in_review",
    "prepare_failed",
    "publishing",
    "publish_failed",
)
AI_TASK_STATUSES = ("queued", "running", "succeeded", "failed")
PREPARATION_STATUSES = ("succeeded", "failed")


def _in(column: str, values: tuple[str, ...]) -> str:
    joined = ", ".join(f"'{v}'" for v in values)
    return f"{column} IN ({joined})"


def _now() -> sa.sql.elements.ColumnElement:
    return sa.func.now()


def upgrade() -> None:
    op.create_table(
        "queue_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_kind", sa.String(length=32), nullable=False),
        sa.Column("source_url", sa.Text()),
        sa.Column("normalized_url", sa.Text()),
        sa.Column("note", sa.Text()),
        sa.Column("channel", sa.String(length=32), nullable=False, server_default="manual"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="received"),
        sa.Column("submitted_by", sa.String(length=128)),
        sa.Column(
            "submitted_at", sa.DateTime(timezone=True), server_default=_now(), nullable=False
        ),
        sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.Column("commit_ref", sa.String(length=64)),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=_now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=_now(), nullable=False
        ),
        sa.CheckConstraint(_in("status", ITEM_STATUSES), name="ck_queue_items_status"),
    )
    op.create_index("ix_queue_items_status", "queue_items", ["status"])
    # 발행 전 같은 URL 은 새 항목이 아니라 기존 항목에 합류한다(SPEC-007 S-4).
    op.create_index(
        "uq_queue_items_pending_url",
        "queue_items",
        ["normalized_url"],
        unique=True,
        postgresql_where=sa.text(
            "normalized_url IS NOT NULL AND deleted_at IS NULL AND "
            + _in("status", ITEM_PENDING_STATUSES)
        ),
    )

    op.create_table(
        "ai_tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="queued"),
        sa.Column("retry_of_task_id", sa.Integer()),
        sa.Column("session_ref", sa.String(length=128)),
        sa.Column("external_task_ref", sa.String(length=128)),
        sa.Column("error_code", sa.String(length=64)),
        sa.Column("error_message", sa.Text()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=_now(), nullable=False
        ),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.CheckConstraint(_in("status", AI_TASK_STATUSES), name="ck_ai_tasks_status"),
        sa.ForeignKeyConstraint(
            ["item_id"], ["queue_items.id"], name="fk_ai_tasks_item", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["retry_of_task_id"], ["ai_tasks.id"], name="fk_ai_tasks_retry_of"),
    )
    op.create_index("ix_ai_tasks_item_id", "ai_tasks", ["item_id"])

    op.create_table(
        "item_preparations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("ai_task_id", sa.Integer()),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=_now(), nullable=False
        ),
        sa.CheckConstraint(
            _in("status", PREPARATION_STATUSES), name="ck_item_preparations_status"
        ),
        sa.ForeignKeyConstraint(
            ["item_id"],
            ["queue_items.id"],
            name="fk_item_preparations_item",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["ai_task_id"], ["ai_tasks.id"], name="fk_item_preparations_ai_task"
        ),
    )
    op.create_index(
        "uq_item_preparations_version",
        "item_preparations",
        ["item_id", "version"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("uq_item_preparations_version", table_name="item_preparations")
    op.drop_table("item_preparations")
    op.drop_index("ix_ai_tasks_item_id", table_name="ai_tasks")
    op.drop_table("ai_tasks")
    op.drop_index("uq_queue_items_pending_url", table_name="queue_items")
    op.drop_index("ix_queue_items_status", table_name="queue_items")
    op.drop_table("queue_items")
