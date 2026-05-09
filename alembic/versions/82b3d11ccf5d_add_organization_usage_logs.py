"""add organization usage logs

Revision ID: 82b3d11ccf5d
Revises: f5099cea1774
Create Date: 2026-05-09 23:42:50.003928
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "82b3d11ccf5d"
down_revision: Union[str, Sequence[str], None] = "f5099cea1774"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "organization_usage_logs",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("agent_slug", sa.String(), nullable=False),
        sa.Column("request_type", sa.String(), nullable=False, server_default="analysis"),
        sa.Column("credits_used", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("organization_usage_logs")