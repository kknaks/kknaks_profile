"""잔디가 추적할 레포 레지스트리 (KDEV-WORK-017 P5 / KDEV-SPEC-011)

**"보여줄 레포" 와 "긁을 레포" 를 분리한다.** 종전에는 추적 대상이
`products/*/showcase.md` 에 묶여 있었다 — 그 파일은 공개 표시용이라, 사이트에
안 보이지만 커밋은 세고 싶은 레포를 표현할 방법이 없었다.

이 파이프라인에서 유일한 스키마 변경이다. 큐·게이트 테이블은 손대지 않는다 —
`source_kind` 와 `stage_name` 에 CHECK 가 없어 새 파이프라인이 스키마를 건드리지
않기 때문이다(정의는 데이터다, KDEV-DEC-011 D2).

Revision ID: 0007_tracked_repos
Revises: 0006_preparation_running
Create Date: 2026-08-01
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0007_tracked_repos"
down_revision: Union[str, None] = "0006_preparation_running"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tracked_repos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(160), nullable=False),
        sa.Column("type", sa.String(16), nullable=False),
        sa.Column("detail", sa.String(80)),
        sa.Column("account", sa.String(16), nullable=False, server_default="personal"),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("path_rules", postgresql.JSONB()),
        sa.Column("last_fetched_at", sa.DateTime(timezone=True)),
        sa.Column("last_error", sa.Text()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("type IN ('company', 'studio')", name="ck_tracked_repos_type"),
        sa.CheckConstraint(
            "account IN ('personal', 'company')", name="ck_tracked_repos_account"
        ),
        # career 귀속의 불변을 DB 가 강제한다. 앱에만 두면 조용히 틀린 채로 쌓인다.
        sa.CheckConstraint(
            "(type = 'company' AND detail IS NOT NULL)"
            " OR (type = 'studio' AND detail IS NULL)",
            name="ck_tracked_repos_detail",
        ),
    )
    op.create_index("uq_tracked_repos_slug", "tracked_repos", ["slug"], unique=True)


def downgrade() -> None:
    # 되돌리면 추적 대상이 사라진다. 클론은 볼륨에 남아 있으므로 다시 등록하면
    # 재클론 없이 이어진다 — 그래서 테이블만 지운다.
    op.drop_index("uq_tracked_repos_slug", table_name="tracked_repos")
    op.drop_table("tracked_repos")
