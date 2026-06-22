"""fake base

Revision ID: 3fd35d329484
Revises: 5adf5372458b
Create Date: 2026-06-17 21:20:47.987939

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fd35d329484'
down_revision: Union[str, Sequence[str], None] = '5adf5372458b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
