"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-07-01 00:00:00

Creates: users, consent_records, sessions, turns, feedback.
Portable across Postgres and SQLite via GUID + PortableJSON columns.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from api.db.models import GUID, PortableJSON


revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("email", sa.String(320), unique=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "sessions",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("user_id", GUID(),
                  sa.ForeignKey("users.id", ondelete="CASCADE"),
                  nullable=True),
        sa.Column("consent_id", GUID(), nullable=True),  # FK added after consent_records
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("last_active", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_sessions_last_active", "sessions", ["last_active"])

    op.create_table(
        "consent_records",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("session_id", GUID(),
                  sa.ForeignKey("sessions.id", ondelete="SET NULL"),
                  nullable=True),
        sa.Column("user_id", GUID(),
                  sa.ForeignKey("users.id", ondelete="CASCADE"),
                  nullable=True),
        sa.Column("policy_version", sa.String(16), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("ip_hash", sa.String(64), nullable=True),
        sa.Column("user_agent_hash", sa.String(64), nullable=True),
    )

    # Now add the FK from sessions.consent_id -> consent_records.id
    with op.batch_alter_table("sessions") as batch:
        batch.create_foreign_key(
            "fk_sessions_consent",
            "consent_records", ["consent_id"], ["id"],
            ondelete="SET NULL",
        )

    op.create_table(
        "turns",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("session_id", GUID(),
                  sa.ForeignKey("sessions.id", ondelete="CASCADE"),
                  nullable=False),
        sa.Column("ts", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("user_hash", sa.String(64), nullable=False),
        sa.Column("user_message", sa.Text, nullable=True),
        sa.Column("response", sa.Text, nullable=False),
        sa.Column("safety_route", sa.String(64), nullable=False),
        sa.Column("intent_module", sa.String(32), nullable=False),
        sa.Column("safety_json", PortableJSON(), nullable=True),
        sa.Column("intent_json", PortableJSON(), nullable=True),
        sa.Column("critic_json", PortableJSON(), nullable=True),
        sa.Column("timing_ms_json", PortableJSON(), nullable=True),
        sa.Column("retention_ends_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("idx_turns_session_id", "turns", ["session_id"])
    op.create_index("idx_turns_ts", "turns", ["ts"])

    op.create_table(
        "feedback",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("turn_id", GUID(),
                  sa.ForeignKey("turns.id", ondelete="CASCADE"),
                  nullable=False),
        sa.Column("session_id", GUID(), nullable=True),
        sa.Column("verdict", sa.String(20), nullable=False),
        sa.Column("comment", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("review_note", sa.Text, nullable=True),
    )
    op.create_index("idx_feedback_turn_id", "feedback", ["turn_id"])
    op.create_index("idx_feedback_verdict", "feedback", ["verdict"])


def downgrade() -> None:
    op.drop_index("idx_feedback_verdict", table_name="feedback")
    op.drop_index("idx_feedback_turn_id", table_name="feedback")
    op.drop_table("feedback")

    op.drop_index("idx_turns_ts", table_name="turns")
    op.drop_index("idx_turns_session_id", table_name="turns")
    op.drop_table("turns")

    with op.batch_alter_table("sessions") as batch:
        batch.drop_constraint("fk_sessions_consent", type_="foreignkey")

    op.drop_table("consent_records")

    op.drop_index("idx_sessions_last_active", table_name="sessions")
    op.drop_table("sessions")

    op.drop_table("users")
