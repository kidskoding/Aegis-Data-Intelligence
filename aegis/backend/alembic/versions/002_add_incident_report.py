"""Add report column to incidents table.

Revision ID: 002
Revises: 001
Create Date: 2026-02-17
"""

from alembic import op
import sqlalchemy as sa

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("incidents", sa.Column("report", sa.Text, nullable=True))


def downgrade() -> None:
    op.drop_column("incidents", "report")
