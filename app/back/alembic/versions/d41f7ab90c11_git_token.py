"""git_token 표 신설 + repo.account → repo.git_token_id

토큰 슬롯(env 고정 personal/company)을 버리고 토큰을 행으로 만든다 —
개인 n개·회사 n개. 토큰은 Fernet 암호문, 키는 .env GIT_TOKEN_KEY.
repo.account 는 쓰인 적 없이(전부 NULL) 같은 날 교체됐다 — 데이터 이관 없음.

Revision ID: d41f7ab90c11
Revises: c3d1a90b52aa
Create Date: 2026-08-25
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "d41f7ab90c11"
down_revision = "c3d1a90b52aa"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "git_token",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("kind", sa.String(length=16), nullable=False),
        sa.Column("account", sa.String(length=64), nullable=False),
        sa.Column("token_cipher", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.drop_column("repo", "account")
    op.add_column("repo", sa.Column("git_token_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_repo_git_token", "repo", "git_token", ["git_token_id"], ["id"], ondelete="SET NULL"
    )


def downgrade() -> None:
    op.drop_constraint("fk_repo_git_token", "repo", type_="foreignkey")
    op.drop_column("repo", "git_token_id")
    op.add_column("repo", sa.Column("account", sa.String(length=16), nullable=True))
    op.drop_table("git_token")
