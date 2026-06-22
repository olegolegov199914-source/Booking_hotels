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
    # 1. Добавляем новую колонку с правильной формулой
    op.execute("""
        ALTER TABLE bookings 
        ADD COLUMN total_cost_new numeric 
        GENERATED ALWAYS AS (EXTRACT(DAY FROM (date_to - date_from)) * price) STORED;
    """)
    # 2. Удаляем старую колонку
    op.execute("ALTER TABLE bookings DROP COLUMN total_cost;")
    # 3. Переименовываем новую колонку
    op.execute("ALTER TABLE bookings RENAME COLUMN total_cost_new TO total_cost;")

def downgrade():
    # Откат – аналогично в обратном порядке
    op.execute("ALTER TABLE bookings ADD COLUMN total_cost_old numeric GENERATED ALWAYS AS (EXTRACT(DAY FROM (date_from - date_to)) * price) STORED;")
    op.execute("ALTER TABLE bookings DROP COLUMN total_cost;")
    op.execute("ALTER TABLE bookings RENAME COLUMN total_cost_old TO total_cost;")