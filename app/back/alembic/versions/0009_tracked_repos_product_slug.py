"""레포 → 제품 조인 컬럼 (KDEV-WORK-018 P2 / KDEV-DEC-017 D1)

제품(`products/{slug}/`)·프로젝트(`showcase.md`)·커리어(`persona/career/`)가 같은
커밋에서 나오는데 셋을 잇는 키가 없었다. `detail` 이 company 를 career 로 보내듯
`product_slug` 가 레포를 제품으로 보낸다.

**컬럼 하나로 끝나는 이유는 본문이 md 에 남기 때문이다.** 공개 카드는 파일이 SoT 라
DB 가 담을 것은 조인과 운영 상태뿐이고, 그래서 별도 `projects` 테이블이 필요 없다.

**CHECK 를 걸지 않는다.** 실재하는 디렉토리인지는 DB 가 알 수 없다. 걸면 디렉토리명이
바뀔 때마다 마이그레이션이 따라붙고, DB 계층이 레포 파일시스템을 알게 된다(D7).

nullable 이라 **기존 13행은 NULL 로 시작하고 시드가 채운다.** 아무도 읽지 않는 컬럼이라
이 리비전만 올리고 뒤를 되돌려도 잔디 경로는 그대로 돈다.

Revision ID: 0009_tracked_repos_product_slug
Revises: 0008_item_no_activity
Create Date: 2026-08-03
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0009_tracked_repos_product_slug"
down_revision: Union[str, None] = "0008_item_no_activity"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tracked_repos",
        sa.Column("product_slug", sa.String(64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("tracked_repos", "product_slug")
