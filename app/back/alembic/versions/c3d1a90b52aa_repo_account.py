"""repo.account — GitHub 토큰 슬롯 (personal / company)

계정·토큰의 실체는 .env(GH_TOKEN_PERSONAL / GH_TOKEN_COMPANY)가 갖고,
행은 어느 슬롯을 쓸지만 고른다 — 이직해도 DB 는 안 바뀐다. NULL 은 무토큰.

Revision ID: c3d1a90b52aa
Revises: 7524172cea2b
Create Date: 2026-08-25
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "c3d1a90b52aa"
down_revision = "7524172cea2b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("repo", sa.Column("account", sa.String(length=16), nullable=True))


def downgrade() -> None:
    op.drop_column("repo", "account")
