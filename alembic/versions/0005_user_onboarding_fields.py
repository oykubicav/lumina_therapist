"""users tablosuna onboarding alanları

Ad ve konu seçimi localStorage'da tutuluyordu. İki sorunu vardı: cihaz
değişince kayboluyordu, ve geçici bir ağ hatası kullanıcıyı düşürdüğünde
profil sahibi eşleşmediği için siliniyordu — bu da onboarding'in her
girişte tekrar çıkmasına yol açıyordu. Hesaba ait veri hesapla dursun.

Revision ID: 0005_user_onboarding_fields
Revises: 23a403349e69
"""
from alembic import op
import sqlalchemy as sa


revision = "0005_user_onboarding_fields"
down_revision = "23a403349e69"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("display_name", sa.String(60), nullable=True))
    op.add_column("users", sa.Column("focus_topics", sa.JSON(), nullable=True))
    op.add_column(
        "users",
        sa.Column("onboarded_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "onboarded_at")
    op.drop_column("users", "focus_topics")
    op.drop_column("users", "display_name")
