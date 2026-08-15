"""Add model_version, boundary_state, retrieved_card_ids to turns.

AI Act transparency — traceability for each turn.

Revision ID: 0004_transparency_fields
Revises: 0003_assessments
Create Date: 2026-07-24
"""
from alembic import op
import sqlalchemy as sa
from api.db.models import PortableJSON

revision = "0004_transparency_fields"
down_revision = "0003_assessments"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("turns", sa.Column("model_version", sa.String(64), nullable=True))
    op.add_column("turns", sa.Column("boundary_state", sa.String(16), nullable=True))
    op.add_column("turns", sa.Column("retrieved_card_ids", PortableJSON(), nullable=True))


def downgrade():
    op.drop_column("turns", "retrieved_card_ids")
    op.drop_column("turns", "boundary_state")
    op.drop_column("turns", "model_version")
