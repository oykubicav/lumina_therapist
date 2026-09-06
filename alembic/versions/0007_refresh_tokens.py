"""refresh_tokens tablosu

Tek ve uzun ömürlü access token yerine access + refresh ikilisi. Refresh
token httpOnly çerezde taşınacağı için JavaScript okuyamıyor; sunucuda
kaydı olduğu için iptal edilebiliyor — tek token'lı halde çıkış yapmak
yalnızca tarayıcıdaki kopyayı siliyordu.

Ham token saklanmıyor, SHA-256 hash'i tutuluyor.

Revision ID: 0007_refresh_tokens
Revises: 0006_focus_greeted
"""
from alembic import op
import sqlalchemy as sa

# GUID modelden geliyor: Postgres'te UUID, SQLite'ta CHAR(36) oluyor.
# Ham CHAR(36) yazmak Postgres'te users.id (UUID) ile foreign key
# kurulmasını engelliyor — tipler uyuşmuyor.
from api.db.models import GUID


revision = "0007_refresh_tokens"
down_revision = "0006_focus_greeted"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "refresh_tokens",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column(
            "user_id",
            GUID(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("token_hash", sa.String(64), nullable=False, unique=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("replaced_by", GUID(), nullable=True),
        sa.Column("user_agent", sa.String(200), nullable=True),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("idx_refresh_tokens_user_id", "refresh_tokens", ["user_id"])
    op.create_index("idx_refresh_tokens_hash", "refresh_tokens", ["token_hash"])


def downgrade() -> None:
    op.drop_index("idx_refresh_tokens_hash", table_name="refresh_tokens")
    op.drop_index("idx_refresh_tokens_user_id", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")
