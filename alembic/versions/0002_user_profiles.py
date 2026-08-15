"""Add user_profiles table — longitudinal structured memory.

Revision ID: 0002_user_profiles
Revises: 0001_initial
Create Date: 2026-07-24
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from api.db.models import GUID, PortableJSON

# revision identifiers
revision = "0002_user_profiles"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_profiles",
        sa.Column("id", GUID(), nullable=False),
        sa.Column("session_id", GUID(), nullable=False),
        sa.Column("user_id", GUID(), nullable=True),
        sa.Column("turn_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("triggers", PortableJSON(), nullable=True),
        sa.Column("themes", PortableJSON(), nullable=True),
        sa.Column("coping_tried", PortableJSON(), nullable=True),
        sa.Column("modules_engaged", PortableJSON(), nullable=True),
        sa.Column("progress_notes", PortableJSON(), nullable=True),
        sa.Column("last_summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_id", name="uq_user_profiles_session_id"),
    )
    op.create_index("idx_user_profiles_session_id", "user_profiles", ["session_id"])


def downgrade():
    op.drop_index("idx_user_profiles_session_id", table_name="user_profiles")
    op.drop_table("user_profiles")
