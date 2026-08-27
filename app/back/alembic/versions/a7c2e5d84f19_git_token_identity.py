"""git_token — email 추가

토큰 등록이 email / account / token 을 받는다 — email 은 나중에 착지 커밋의
git 신원(user.email)에 쓴다. 기존 행이 있을 수 있어 email 은
server_default '' 로 채워 NOT NULL 을 만든 뒤 default 를 뗀다.

Revision ID: a7c2e5d84f19
Revises: d41f7ab90c11
Create Date: 2026-08-25
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "a7c2e5d84f19"
down_revision = "d41f7ab90c11"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "git_token",
        sa.Column("email", sa.String(length=255), nullable=False, server_default=""),
    )
    op.alter_column("git_token", "email", server_default=None)


def downgrade() -> None:
    op.drop_column("git_token", "email")
