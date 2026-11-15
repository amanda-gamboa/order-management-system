"""add server defaults to active status fields

Revision ID: 55474eadb512
Revises: 884fd917bdba
Create Date: 2026-11-15 22:39:36.893068

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "55474eadb512"
down_revision: Union[str, Sequence[str], None] = "884fd917bdba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column(
        "customers",
        "is_active",
        existing_type=mysql.TINYINT(display_width=1),
        server_default=sa.text("true"),
        existing_nullable=False,
    )
    op.alter_column(
        "products",
        "is_active",
        existing_type=mysql.TINYINT(display_width=1),
        server_default=sa.text("true"),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "products",
        "is_active",
        existing_type=mysql.TINYINT(display_width=1),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        "customers",
        "is_active",
        existing_type=mysql.TINYINT(display_width=1),
        server_default=None,
        existing_nullable=False,
    )
