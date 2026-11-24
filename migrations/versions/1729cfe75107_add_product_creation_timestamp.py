"""add product creation timestamp

Revision ID: 1729cfe75107
Revises: 35f8a9476ad0
Create Date: 2026-11-24 15:00:33.812926

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "1729cfe75107"
down_revision: Union[str, Sequence[str], None] = "35f8a9476ad0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "products",
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("products", "created_at")
