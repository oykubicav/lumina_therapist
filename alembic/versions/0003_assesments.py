"""Add assessments table — PHQ-9 / GAD-7 clinical measurement.

Revision ID: 0003_assessments
Revises: 0002_user_profiles
Create Date: 2026-07-24
"""
from alembic import op
import sqlalchemy as sa
from api.db.models import GUID, PortableJSON

revision = "0003_assessments"
down_revision = "0002_user_profiles"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "assessments",
        sa.Column("id", GUID(), nullable=False),
        sa.Column("session_id", GUID(), nullable=False),
        sa.Column("user_id", GUID(), nullable=True),
        sa.Column("kind", sa.String(8), nullable=False),
        sa.Column("answers", PortableJSON(), nullable=False),
        sa.Column("total_score", sa.Integer(), nullable=False),
        sa.Column("severity", sa.String(24), nullable=False),
        sa.Column("suicide_flag", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("taken_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_assessments_session_id", "assessments", ["session_id"])
    op.create_index("idx_assessments_kind", "assessments", ["kind"])
    op.create_index("idx_assessments_taken_at", "assessments", ["taken_at"])


def downgrade():
    op.drop_index("idx_assessments_taken_at", table_name="assessments")
    op.drop_index("idx_assessments_kind", table_name="assessments")
    op.drop_index("idx_assessments_session_id", table_name="assessments")
    op.drop_table("assessments")