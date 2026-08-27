"""company — github_org 추가

회사 등록 때 GitHub 조직(owner)을 텍스트로 사전 등록한다 —
레포 등록 화면의 owner 드롭다운 후보가 된다. nullable — 조직이 없는
회사도 있다.

Revision ID: c8e4f7a91b23
Revises: f3a8b1c92d47
Create Date: 2026-08-25
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "c8e4f7a91b23"
down_revision = "f3a8b1c92d47"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("company", sa.Column("github_org", sa.String(64), nullable=True))


def downgrade() -> None:
    op.drop_column("company", "github_org")
