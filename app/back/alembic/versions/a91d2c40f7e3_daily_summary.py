"""daily_summary — commit.summarized_at + daily 표

Revision ID: a91d2c40f7e3
Revises: d5f8a02c7b31
Create Date: 2026-08-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a91d2c40f7e3'
down_revision: Union[str, Sequence[str], None] = 'd5f8a02c7b31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'commit',
        sa.Column('summarized_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        'daily',
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('date'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('daily')
    op.drop_column('commit', 'summarized_at')
