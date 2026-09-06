"""Refresh token üretimi, rotasyon ve yeniden kullanım tespiti.

Bu katman uçlardan bağımsız test ediliyor: HTTP, çerez ve CSRF ayrı
konular, buradaki soru sadece "token mantığı doğru mu".
"""

import uuid
from datetime import timedelta

import pytest

from api.auth import refresh_tokens as rt


def _user(email: str | None = None) -> uuid.UUID:
    from api import db as _db
    from api.db.models import User

    with _db.get_sessionmaker()() as s, s.begin():
        u = User(
            email=email or f"rt-{uuid.uuid4().hex[:8]}@test.com",
            password_hash="x",
            email_verified=True,
        )
        s.add(u)
        s.flush()
        uid = u.id
    return uid


@pytest.fixture()
def db(app):
    from api import db as _db
    with _db.get_sessionmaker()() as s:
        yield s


def test_raw_token_not_stored(db, app):
    """Veritabanında ham token bulunmamalı — yalnızca hash."""
    from api.db.models import RefreshToken

    uid = _user()
    raw = rt.issue(db, uid)
    db.commit()

    row = db.query(RefreshToken).one()
    assert row.token_hash != raw
    assert len(row.token_hash) == 64
    assert row.token_hash == rt.hash_token(raw)


def test_rotate_returns_new_token(db, app):
    uid = _user()
    first = rt.issue(db, uid)
    db.commit()

    sonuc, user_id, second = rt.rotate(db, first)
    db.commit()

    assert sonuc == rt.RefreshOutcome.OK
    assert user_id == uid
    assert second is not None
    assert second != first


def test_old_token_closed_after_rotation(db, app):
    from api.db.models import RefreshToken

    uid = _user()
    first = rt.issue(db, uid)
    db.commit()
    _, _, second = rt.rotate(db, first)
    db.commit()

    eski = db.query(RefreshToken).filter_by(token_hash=rt.hash_token(first)).one()
    yeni = db.query(RefreshToken).filter_by(token_hash=rt.hash_token(second)).one()

    assert eski.revoked_at is not None
    assert eski.replaced_by == yeni.id
    assert yeni.revoked_at is None


def test_unknown_token_invalid(db, app):
    sonuc, user_id, yeni = rt.rotate(db, "uydurma-token")
    assert sonuc == rt.RefreshOutcome.INVALID
    assert user_id is None
    assert yeni is None


def test_expired_token_invalid(db, app):
    from api.db.models import RefreshToken

    uid = _user()
    raw = rt.issue(db, uid)
    row = db.query(RefreshToken).one()
    row.expires_at = rt._now() - timedelta(days=1)
    db.commit()

    sonuc, _, yeni = rt.rotate(db, raw)
    assert sonuc == rt.RefreshOutcome.INVALID
    assert yeni is None


def _age_revocation(db, raw: str, seconds: int) -> None:
    """İptal zamanını geriye al — hoşgörü penceresinin dışına çıkarmak için."""
    from api.db.models import RefreshToken

    row = db.query(RefreshToken).filter_by(token_hash=rt.hash_token(raw)).one()
    row.revoked_at = rt._now() - timedelta(seconds=seconds)
    db.commit()


def test_reuse_detected_and_all_sessions_dropped(db, app):
    """Asıl güvenlik davranışı: çalıntı token tekrar kullanılırsa her şey düşer."""
    from api.db.models import RefreshToken

    uid = _user()

    # İki ayrı cihaz
    telefon = rt.issue(db, uid, user_agent="iPhone")
    dizustu = rt.issue(db, uid, user_agent="Mac")
    db.commit()

    # Telefon normal şekilde yeniliyor
    _, _, telefon2 = rt.rotate(db, telefon)
    db.commit()

    # Saldırgan eski telefon token'ını ele geçirmiş. Yarış değil, sonradan
    # deneniyor — hoşgörü penceresinin dışına çıkar.
    _age_revocation(db, telefon, rt.REUSE_GRACE_SECONDS + 60)

    sonuc, user_id, yeni = rt.rotate(db, telefon)
    db.commit()

    assert sonuc == rt.RefreshOutcome.REUSE
    assert user_id == uid
    assert yeni is None

    # Kullanıcının bütün oturumları kapanmış olmalı — dizüstü dahil
    acik = db.query(RefreshToken).filter_by(user_id=uid, revoked_at=None).count()
    assert acik == 0

    # Yenilenmiş telefon token'ı da artık geçmiyor
    _age_revocation(db, telefon2, rt.REUSE_GRACE_SECONDS + 60)
    assert rt.rotate(db, telefon2)[0] == rt.RefreshOutcome.REUSE


def test_race_does_not_drop_sessions(db, app):
    """İki sekme aynı anda yenilerse kullanıcı düşmemeli.

    İkinci istek iptal edilmiş token'la geliyor ama iptal saniyeler önce
    olmuş ve yerine geçen kayıt var — saldırı değil, yarış.
    """
    from api.db.models import RefreshToken

    uid = _user()
    telefon = rt.issue(db, uid, user_agent="iPhone")
    dizustu = rt.issue(db, uid, user_agent="Mac")
    db.commit()

    # Sekme 1 yeniliyor
    _, _, yeni = rt.rotate(db, telefon)
    db.commit()

    # Sekme 2 aynı eski çerezle geliyor
    sonuc, user_id, verilen = rt.rotate(db, telefon)
    db.commit()

    assert sonuc == rt.RefreshOutcome.RACE
    assert user_id == uid
    assert verilen is None

    # Kritik: hiçbir oturum düşmemiş olmalı
    acik = db.query(RefreshToken).filter_by(user_id=uid, revoked_at=None).count()
    assert acik == 2                      # yeni telefon token'ı + dizüstü
    assert rt.rotate(db, dizustu)[0] == rt.RefreshOutcome.OK


def test_race_window_expires(db, app):
    """Pencere dolduktan sonra aynı token artık saldırı sayılıyor."""
    uid = _user()
    raw = rt.issue(db, uid)
    db.commit()
    rt.rotate(db, raw)
    db.commit()

    assert rt.rotate(db, raw)[0] == rt.RefreshOutcome.RACE

    _age_revocation(db, raw, rt.REUSE_GRACE_SECONDS + 1)
    assert rt.rotate(db, raw)[0] == rt.RefreshOutcome.REUSE


def test_reuse_does_not_touch_other_users(db, app):
    uid_a = _user()
    uid_b = _user()

    a1 = rt.issue(db, uid_a)
    b1 = rt.issue(db, uid_b)
    db.commit()

    rt.rotate(db, a1)
    db.commit()
    rt.rotate(db, a1)          # yeniden kullanım
    db.commit()

    # B'nin oturumu etkilenmemeli
    sonuc, user_id, yeni = rt.rotate(db, b1)
    assert sonuc == rt.RefreshOutcome.OK
    assert user_id == uid_b
    assert yeni is not None


def test_revoke_one_closes_only_that_session(db, app):
    from api.db.models import RefreshToken

    uid = _user()
    telefon = rt.issue(db, uid, user_agent="iPhone")
    dizustu = rt.issue(db, uid, user_agent="Mac")
    db.commit()

    assert rt.revoke_one(db, telefon) is True
    db.commit()

    assert rt.rotate(db, dizustu)[0] == rt.RefreshOutcome.OK
    assert db.query(RefreshToken).filter_by(
        token_hash=rt.hash_token(telefon)
    ).one().revoked_at is not None


def test_revoke_one_idempotent(db, app):
    uid = _user()
    raw = rt.issue(db, uid)
    db.commit()

    assert rt.revoke_one(db, raw) is True
    db.commit()
    assert rt.revoke_one(db, raw) is False


def test_revoke_all_counts_only_open(db, app):
    uid = _user()
    a = rt.issue(db, uid)
    rt.issue(db, uid)
    rt.issue(db, uid)
    db.commit()

    rt.revoke_one(db, a)
    db.commit()

    assert rt.revoke_all_for_user(db, uid) == 2


def test_user_agent_truncated(db, app):
    from api.db.models import RefreshToken

    uid = _user()
    rt.issue(db, uid, user_agent="x" * 500)
    db.commit()

    assert len(db.query(RefreshToken).one().user_agent) == 200


def test_purge_keeps_revoked_rows_for_detection(db, app):
    """Temizlik, yeniden kullanım tespitini bozmamalı.

    İptal edilmiş satır silinirse çalıntı token 'bilinmeyen' görünür ve
    REUSE yerine INVALID döner — yani tespit sessizce kapanır.
    """
    from api.db.models import RefreshToken

    uid = _user()
    ilk = rt.issue(db, uid)
    db.commit()
    rt.rotate(db, ilk)          # ilk satır iptal edildi
    db.commit()

    assert rt.purge_expired(db) == 0
    db.commit()

    # Satır duruyor ve tespit hâlâ çalışıyor
    assert db.query(RefreshToken).filter_by(token_hash=rt.hash_token(ilk)).count() == 1
    _age_revocation(db, ilk, rt.REUSE_GRACE_SECONDS + 60)
    assert rt.rotate(db, ilk)[0] == rt.RefreshOutcome.REUSE


def test_purge_drops_old_revoked_rows(db, app):
    from api.db.models import RefreshToken

    uid = _user()
    raw = rt.issue(db, uid)
    db.commit()
    rt.revoke_one(db, raw)
    db.commit()

    row = db.query(RefreshToken).one()
    row.revoked_at = rt._now() - timedelta(days=rt.REUSE_DETECTION_DAYS + 1)
    db.commit()

    assert rt.purge_expired(db) == 1
    db.commit()
    assert db.query(RefreshToken).count() == 0


def test_purge_drops_unused_expired_rows(db, app):
    """Hiç kullanılmamış, süresi dolmuş satırın tespit değeri yok."""
    from api.db.models import RefreshToken

    uid = _user()
    rt.issue(db, uid)
    db.commit()

    row = db.query(RefreshToken).one()
    row.expires_at = rt._now() - timedelta(days=1)
    db.commit()

    assert rt.purge_expired(db) == 1
    db.commit()
    assert db.query(RefreshToken).count() == 0


def test_purge_leaves_active_rows_alone(db, app):
    from api.db.models import RefreshToken

    uid = _user()
    rt.issue(db, uid)
    rt.issue(db, uid)
    db.commit()

    assert rt.purge_expired(db) == 0
    db.commit()
    assert db.query(RefreshToken).count() == 2


def test_tokens_are_unique(db, app):
    uid = _user()
    uretilen = {rt.issue(db, uid) for _ in range(20)}
    db.commit()
    assert len(uretilen) == 20
