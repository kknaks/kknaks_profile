"""career — persona_path 추가

역할별 persona md(DB 파생물)의 위치. erd 의 career 는 원장(detail_path)이 없다 —
이건 「DB 를 통째로 렌더해 매일 덮어쓰는 파생 md」의 경로라 detail_path 와 별개다.
nullable — 비어 있으면 렌더가 회사 slug·역할 title 로 경로를 파생한다.

Revision ID: f1c0a9b2d3e4
Revises: a91d2c40f7e3
Create Date: 2026-08-26
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "f1c0a9b2d3e4"
down_revision = "a91d2c40f7e3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("career", sa.Column("persona_path", sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column("career", "persona_path")
