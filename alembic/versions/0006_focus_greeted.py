"""users.focus_greeted_at

Onboarding'de seçilen konular karşılama metninde yalnızca bir kez anılmalı.
Bu bayrak localStorage'daydı ve çıkış-giriş döngüsünde siliniyordu; sonuç
olarak her yeni sohbette aynı "başlarken şunları demiştin" cümlesi
kuruluyordu. Hesapla birlikte dursun.

Revision ID: 0006_focus_greeted
Revises: 0005_user_onboarding_fields
"""
from alembic import op
import sqlalchemy as sa


revision = "0006_focus_greeted"
down_revision = "0005_user_onboarding_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("focus_greeted_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "focus_greeted_at")
