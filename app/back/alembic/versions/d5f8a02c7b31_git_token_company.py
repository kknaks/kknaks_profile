"""git_token — company_id 추가

kind=company 토큰의 소속 회사. nullable — personal 은 NULL 이고,
기존 company 행도 NULL 로 남아 화면에서 연결한다. 회사 삭제 시 SET NULL —
토큰 행(레포 연결)은 살아남는다.

Revision ID: d5f8a02c7b31
Revises: c8e4f7a91b23
Create Date: 2026-08-25
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "d5f8a02c7b31"
down_revision = "c8e4f7a91b23"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("git_token", sa.Column("company_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_git_token_company",
        "git_token",
        "company",
        ["company_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_git_token_company", "git_token", type_="foreignkey")
    op.drop_column("git_token", "company_id")
