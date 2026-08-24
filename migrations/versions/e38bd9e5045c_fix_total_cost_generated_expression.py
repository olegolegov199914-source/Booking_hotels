"""fix_total_cost_generated_expression

Revision ID: e38bd9e5045c
Revises: 8a2922671d2e
Create Date: 2026-06-20 11:25:37.471544

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e38bd9e5045c'
down_revision: Union[str, Sequence[str], None] = '8a2922671d2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    pass

def downgrade():
    pass