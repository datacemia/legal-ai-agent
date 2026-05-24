"""create api keys table

Revision ID: fc5661d5bdee
Revises:
Create Date: 2026-05-21 18:23:11.062230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fc5661d5bdee"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "api_keys",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("key_prefix", sa.String(), nullable=False),
        sa.Column("key_hash", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("last_used_at", sa.DateTime(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.Column("revoked_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_api_keys_id"),
        "api_keys",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_api_keys_key_hash"),
        "api_keys",
        ["key_hash"],
        unique=True,
    )
    op.create_index(
        op.f("ix_api_keys_key_prefix"),
        "api_keys",
        ["key_prefix"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_api_keys_key_prefix"),
        table_name="api_keys",
    )
    op.drop_index(
        op.f("ix_api_keys_key_hash"),
        table_name="api_keys",
    )
    op.drop_index(
        op.f("ix_api_keys_id"),
        table_name="api_keys",
    )
    op.drop_table("api_keys")
