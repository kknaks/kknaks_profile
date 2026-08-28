"""product 에 chat_exposed 추가 — 회사 제품 tool (SPEC-017 v0.0.8 §4)

회사 제품은 `project` 가 아니라 `product` 표에 산다(WORK-023 fix3 조사). 전용 tool
2종(`list_company_products` · `get_company_product`)이 생기면서 그 표에도 노출 옵트인
축이 필요해졌다 — career · project · problem 과 **같은 축**이고 새 기계가 아니다.

기본 false. 이미 있는 행도 전부 false 로 시작한다 — 실수의 방향이 「덜 보여줌」이지
「새어 나감」이 아니게(DEC-027 D4 Rationale).

Revision ID: c2e91a7b40d5
Revises: b7d3e1f04a92
Create Date: 2026-08-28
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "c2e91a7b40d5"
down_revision = "b7d3e1f04a92"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "product",
        sa.Column("chat_exposed", sa.Boolean(), server_default="false", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("product", "chat_exposed")
