"""fix business analysis boolean flags

Revision ID: be584db57ebb
Revises: 037d3240d8f3
Create Date: 2026-05-21 18:23:11.062230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be584db57ebb'
down_revision: Union[str, Sequence[str], None] = '037d3240d8f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    pass


def downgrade():
    pass
