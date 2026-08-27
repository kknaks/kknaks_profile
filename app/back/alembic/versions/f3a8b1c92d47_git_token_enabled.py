"""git_token — enabled 추가

토큰을 지우지 않고 끌 수 있게 한다 — repo.enabled 와 같은 방식.
꺼진 토큰은 수집에서 무토큰 취급(공개 범위만 읽힌다). 기존 행은
server_default true 로 전부 켜진 상태를 유지한다.

Revision ID: f3a8b1c92d47
Revises: a7c2e5d84f19
Create Date: 2026-08-25
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "f3a8b1c92d47"
down_revision = "a7c2e5d84f19"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "git_token",
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default="true"),
    )


def downgrade() -> None:
    op.drop_column("git_token", "enabled")
