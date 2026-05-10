from alembic import op
import sqlalchemy as sa


revision = "3c5060bfa4c5"
down_revision = "82b3d11ccf5d"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "organizations",
        sa.Column("status", sa.String(), nullable=False, server_default="active"),
    )

    op.create_table(
        "organization_agents",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("agent_slug", sa.String(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("organization_id", "agent_slug", name="uq_organization_agent"),
    )


def downgrade():
    op.drop_table("organization_agents")
    op.drop_column("organizations", "status")