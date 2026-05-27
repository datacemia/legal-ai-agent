"""add job queue indexes

Revision ID: ca3c09944d59
Revises: a0e66e2aa655
Create Date: 2026-05-27 20:59:55.126800

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca3c09944d59'
down_revision: Union[str, Sequence[str], None] = 'a0e66e2aa655'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_index(
        "ix_jobs_status_created_at",
        "jobs",
        ["status", "created_at"],
        unique=False,
    )

    op.create_index(
        "ix_jobs_user_id",
        "jobs",
        ["user_id"],
        unique=False,
    )

    op.create_index(
        "ix_jobs_job_type",
        "jobs",
        ["job_type"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index("ix_jobs_job_type", table_name="jobs")
    op.drop_index("ix_jobs_user_id", table_name="jobs")
    op.drop_index("ix_jobs_status_created_at", table_name="jobs")
