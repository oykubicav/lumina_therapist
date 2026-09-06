"""Refresh akışının HTTP tarafı: çerez, CSRF başlığı, rotasyon, çıkış.

Token mantığının kendisi test_refresh_tokens.py'de. Burada sorulan soru
"uçlar doğru davranıyor mu": çerez doğru bayraklarla mı kuruluyor, CSRF
katmanı çalışıyor mu, ve REUSE durumunda iptaller gerçekten veritabanına
yazılıyor mu.

Son madde önemli: iptal işlemi rotate() içinde yapılıyor ama HTTPException
transaction'ın dışında fırlatılıyor. İçeride fırlatılsaydı SQLAlchemy geri
alır ve güvenlik tepkisi sessizce kaybolurdu.
"""

import uuid
from datetime import timedelta

import pytest

from api.auth import refresh_tokens as rt


CLIENT = {"X-Neva-Client": "web"}


def _make_user(email: str, password: str = "parola12345") -> uuid.UUID:
    from api import db as _db
    from api.db.models import User
    from api.auth.passwords import hash_password

    with _db.get_sessionmaker()() as s, s.begin():
        u = User(email=email, password_hash=hash_password(password), email_verified=True)
        s.add(u)
        s.flush()
        uid = u.id
    return uid


@pytest.fixture()
def hesap(client):
    email = f"rf{uuid.uuid4().hex[:8]}@test.com"
    uid = _make_user(email)
    r = client.post("/auth/login", json={"email": email, "password": "parola12345"})
    assert r.status_code == 200, r.text
    return {
        "uid": uid,
        "email": email,
        "access": r.json()["access_token"],
        "cookie": client.cookies.get(rt_cookie_name()),
    }


def rt_cookie_name() -> str:
    from api.auth.cookies import REFRESH_COOKIE_NAME
    return REFRESH_COOKIE_NAME


def _cerezi_degistir(client, value: str) -> None:
    """Jar'ı temizleyip tek çerez bırak.

    httpx'in cookies.set() metodu aynı isimli çerezi değiştirmiyor, ikincisini
    ekliyor. İkisi birden gönderiliyor ve sunucu geçerli olanı görüyor — yani
    "eski çerezle geldi" senaryosu kurulamıyor. Önce temizlemek şart.
    """
    client.cookies.clear()
    client.cookies.set(rt_cookie_name(), value, path="/auth")


def _acik_oturum_sayisi(uid) -> int:
    from api import db as _db
    from api.db.models import RefreshToken

    with _db.get_sessionmaker()() as s:
        return s.query(RefreshToken).filter_by(user_id=uid, revoked_at=None).count()


# ------------------------------------------------------------
# login çerezi
# ------------------------------------------------------------

def test_login_sets_refresh_cookie(client):
    email = f"c{uuid.uuid4().hex[:8]}@test.com"
    _make_user(email)

    r = client.post("/auth/login", json={"email": email, "password": "parola12345"})
    assert r.status_code == 200

    ham = " ".join(r.headers.get_list("set-cookie")).lower()
    assert rt_cookie_name() in ham
    assert "httponly" in ham
    assert "path=/auth" in ham
    assert "samesite=lax" in ham


def test_cookie_secure_defaults_on(monkeypatch):
    """Üretimde Secure zorunlu. Varsayılanın güvenli taraf olması bilinçli:
    env unutulursa üretim korunmuş olur, yerel geliştirme bozulur."""
    import importlib
    import api.auth.cookies as cookies

    monkeypatch.delenv("CBT_COOKIE_SECURE", raising=False)
    yeniden = importlib.reload(cookies)
    try:
        assert yeniden.COOKIE_SECURE is True
    finally:
        monkeypatch.setenv("CBT_COOKIE_SECURE", "0")
        importlib.reload(cookies)


def test_login_does_not_leak_refresh_in_body(client):
    """Refresh token yalnızca çerezde olmalı; gövdeye sızarsa JavaScript okur."""
    email = f"c{uuid.uuid4().hex[:8]}@test.com"
    _make_user(email)

    r = client.post("/auth/login", json={"email": email, "password": "parola12345"})
    assert set(r.json()) == {"access_token", "token_type", "user"}


def test_login_creates_one_session_row(client):
    email = f"c{uuid.uuid4().hex[:8]}@test.com"
    uid = _make_user(email)
    client.post("/auth/login", json={"email": email, "password": "parola12345"})
    assert _acik_oturum_sayisi(uid) == 1


# ------------------------------------------------------------
# CSRF katmanı
# ------------------------------------------------------------

def test_refresh_without_client_header_rejected(client, hesap):
    assert client.post("/auth/refresh").status_code == 403


def test_logout_without_client_header_rejected(client, hesap):
    assert client.post("/auth/logout").status_code == 403


def test_client_header_alone_is_not_enough(client):
    """Başlık var ama çerez yok — yine reddedilmeli."""
    assert client.post("/auth/refresh", headers=CLIENT).status_code == 401


# ------------------------------------------------------------
# rotasyon
# ------------------------------------------------------------

def test_refresh_returns_token_and_user(client, hesap):
    r = client.post("/auth/refresh", headers=CLIENT)
    assert r.status_code == 200
    body = r.json()
    assert body["access_token"]
    assert body["user"]["email"] == hesap["email"]


def test_refresh_rotates_cookie(client, hesap):
    eski = hesap["cookie"]
    r = client.post("/auth/refresh", headers=CLIENT)
    assert r.status_code == 200

    yeni = client.cookies.get(rt_cookie_name())
    assert yeni is not None
    assert yeni != eski


def test_refreshed_access_token_works(client, hesap):
    yeni_access = client.post("/auth/refresh", headers=CLIENT).json()["access_token"]
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {yeni_access}"})
    assert me.status_code == 200
    assert me.json()["email"] == hesap["email"]


def test_refresh_chain_works_repeatedly(client, hesap):
    for _ in range(3):
        assert client.post("/auth/refresh", headers=CLIENT).status_code == 200
    assert _acik_oturum_sayisi(hesap["uid"]) == 1


# ------------------------------------------------------------
# yarış ve yeniden kullanım
# ------------------------------------------------------------

def test_race_returns_409_and_keeps_sessions(client, hesap):
    """İkinci sekme eski çerezle gelirse kullanıcı düşmemeli."""
    eski = hesap["cookie"]
    client.post("/auth/refresh", headers=CLIENT)

    _cerezi_degistir(client, eski)
    r = client.post("/auth/refresh", headers=CLIENT)

    assert r.status_code == 409
    assert _acik_oturum_sayisi(hesap["uid"]) == 1


def test_reuse_drops_all_sessions(client, hesap):
    """Çalıntı token sonradan denenirse tüm oturumlar kapanmalı.

    İptaller transaction içinde yapılıyor, 401 dışarıda fırlatılıyor —
    bu test o ayrımın gerçekten işe yaradığını doğruluyor.
    """
    from api import db as _db
    from api.db.models import RefreshToken

    # İkinci bir cihaz
    client.post("/auth/login", json={"email": hesap["email"], "password": "parola12345"})
    assert _acik_oturum_sayisi(hesap["uid"]) == 2

    eski = hesap["cookie"]
    _cerezi_degistir(client, eski)
    client.post("/auth/refresh", headers=CLIENT)          # normal rotasyon

    # Hoşgörü penceresinin dışına taşı
    with _db.get_sessionmaker()() as s, s.begin():
        row = s.query(RefreshToken).filter_by(token_hash=rt.hash_token(eski)).one()
        row.revoked_at = rt._now() - timedelta(seconds=rt.REUSE_GRACE_SECONDS + 60)

    _cerezi_degistir(client, eski)
    r = client.post("/auth/refresh", headers=CLIENT)

    assert r.status_code == 401
    assert _acik_oturum_sayisi(hesap["uid"]) == 0


def test_unknown_cookie_rejected(client, hesap):
    _cerezi_degistir(client, "uydurma-deger")
    assert client.post("/auth/refresh", headers=CLIENT).status_code == 401


def test_deleted_user_cannot_refresh(client, hesap):
    from api import db as _db
    from api.db.models import User

    with _db.get_sessionmaker()() as s, s.begin():
        s.get(User, hesap["uid"]).deleted_at = rt._now()

    assert client.post("/auth/refresh", headers=CLIENT).status_code == 401


# ------------------------------------------------------------
# çıkış
# ------------------------------------------------------------

def test_logout_revokes_session(client, hesap):
    assert client.post("/auth/logout", headers=CLIENT).status_code == 200
    assert _acik_oturum_sayisi(hesap["uid"]) == 0


def test_logout_makes_refresh_fail(client, hesap):
    client.post("/auth/logout", headers=CLIENT)
    _cerezi_degistir(client, hesap["cookie"])
    assert client.post("/auth/refresh", headers=CLIENT).status_code in (401, 409)


def test_logout_without_cookie_still_ok(client):
    """Çerez yoksa da çıkış başarılı sayılmalı — kullanıcının beklentisi bu."""
    assert client.post("/auth/logout", headers=CLIENT).status_code == 200


def test_logout_only_closes_this_device(client, hesap):
    """Bir cihazdan çıkmak diğerini düşürmemeli."""
    client.post("/auth/login", json={"email": hesap["email"], "password": "parola12345"})
    assert _acik_oturum_sayisi(hesap["uid"]) == 2

    client.post("/auth/logout", headers=CLIENT)
    assert _acik_oturum_sayisi(hesap["uid"]) == 1


def test_logout_all_requires_access_token(client, hesap):
    assert client.post("/auth/logout-all", headers=CLIENT).status_code == 401


def test_logout_all_closes_every_device(client, hesap):
    client.post("/auth/login", json={"email": hesap["email"], "password": "parola12345"})
    client.post("/auth/login", json={"email": hesap["email"], "password": "parola12345"})
    assert _acik_oturum_sayisi(hesap["uid"]) == 3

    r = client.post(
        "/auth/logout-all",
        headers={**CLIENT, "Authorization": f"Bearer {hesap['access']}"},
    )
    assert r.status_code == 200
    assert r.json()["sessions_closed"] == 3
    assert _acik_oturum_sayisi(hesap["uid"]) == 0
