"""fix product name maximum length

Revision ID: 35f8a9476ad0
Revises: 55474eadb512
Create Date: 2026-11-19 20:58:15.426682

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "35f8a9476ad0"
down_revision: Union[str, Sequence[str], None] = "55474eadb512"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column(
        "products",
        "name",
        existing_type=mysql.VARCHAR(length=250),
        type_=sa.String(length=255),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "products",
        "name",
        existing_type=sa.String(length=255),
        type_=mysql.VARCHAR(length=250),
        existing_nullable=False,
    )
