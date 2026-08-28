"""채용담당자 채팅 — chat_session · conversation · chat_message + chat_exposed

SPEC-017 §4 Data Contract / WORK-023 P1.

신규 표 셋(익명 세션 1:N 대화 1:N 메시지)과, 상세 문서를 가진 세 표(career · project ·
problem)의 `chat_exposed` 옵트인 플래그(기본 false — DEC-027 D4)를 한 스텝에 올린다.
롤백은 이 스텝 하나의 downgrade 로 끝난다(WORK-023 Rollback).

Revision ID: b7d3e1f04a92
Revises: f1c0a9b2d3e4
Create Date: 2026-08-28
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "b7d3e1f04a92"
down_revision = "f1c0a9b2d3e4"
branch_labels = None
depends_on = None

# 노출 플래그가 붙는 표 — 상세 문서(또는 상세 본문)를 가진 행들이다.
_EXPOSED_TABLES = ("career", "project", "problem")


def upgrade() -> None:
    op.create_table(
        "chat_session",
        sa.Column("id", sa.Integer(), primary_key=True),
        # 쿠키 값(UUID)의 sha256 hex — 원문은 저장하지 않는다.
        sa.Column("token_hash", sa.String(64), nullable=False),
        sa.Column(
            "last_seen_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("token_hash", name="uq_chat_session_token_hash"),
    )

    op.create_table(
        "conversation",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "session_id",
            sa.Integer(),
            sa.ForeignKey("chat_session.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(64), nullable=False),
        # codex result_session_id — 다음 질문이 resume 으로 넘긴다(DEC-027 D2).
        sa.Column("ai_session_id", sa.String(128), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index(
        "ix_conversation_session",
        "conversation",
        ["session_id", sa.text("created_at DESC")],
    )

    op.create_table(
        "chat_message",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "conversation_id",
            sa.Integer(),
            sa.ForeignKey("conversation.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("role", sa.String(16), nullable=False),
        sa.Column("status", sa.String(16), server_default="done", nullable=False),
        sa.Column("content", sa.Text(), server_default="", nullable=False),
        sa.Column("sources", postgresql.JSONB(), nullable=True),
        sa.Column("steps", postgresql.JSONB(), nullable=True),
        sa.Column("task_id", sa.String(64), nullable=True),
        sa.Column("error_code", sa.String(32), nullable=True),
        sa.Column("turn_token_hash", sa.String(64), nullable=True),
        sa.Column("turn_token_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index(
        "ix_chat_message_conversation", "chat_message", ["conversation_id", "id"]
    )
    # 직렬화 invariant — 한 대화에 pending assistant 는 최대 하나(SPEC-017 §5).
    # 앱의 409 검사가 새는 동시 요청 경로를 DB 가 막는다.
    op.create_index(
        "uq_chat_message_pending",
        "chat_message",
        ["conversation_id"],
        unique=True,
        postgresql_where=sa.text("status = 'pending' AND role = 'assistant'"),
    )
    op.create_index("ix_chat_message_turn_token", "chat_message", ["turn_token_hash"])

    for table in _EXPOSED_TABLES:
        op.add_column(
            table,
            sa.Column(
                "chat_exposed",
                sa.Boolean(),
                server_default="false",
                nullable=False,
            ),
        )


def downgrade() -> None:
    for table in _EXPOSED_TABLES:
        op.drop_column(table, "chat_exposed")
    op.drop_index("ix_chat_message_turn_token", table_name="chat_message")
    op.drop_index("uq_chat_message_pending", table_name="chat_message")
    op.drop_index("ix_chat_message_conversation", table_name="chat_message")
    op.drop_table("chat_message")
    op.drop_index("ix_conversation_session", table_name="conversation")
    op.drop_table("conversation")
    op.drop_table("chat_session")
