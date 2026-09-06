"""Refresh token üretimi, doğrulama ve rotasyonu.

Tasarım kararları:

- Token JWT değil. JWT'nin amacı sunucunun kayıt tutmadan doğrulayabilmesi;
  biz zaten kayıt tutuyoruz (iptal edebilmek için), o yüzden rastgele bir
  dize yeterli.

- Veritabanında ham token yok, SHA-256 hash'i var. Veritabanı sızarsa
  oturumlar ele geçirilemez. Parola hash'lemenin aynı gerekçesi — ama
  bcrypt yerine SHA-256, çünkü token zaten 256 bit rastgele; kaba kuvvet
  saldırısı söz konusu değil ve her istekte hızlı olması gerekiyor.

- Rotasyon: her yenilemede eski satır kapanır, yenisi açılır ve replaced_by
  ile zincir kurulur.

- Yeniden kullanım tespiti: iptal edilmiş bir token tekrar gelirse, birinin
  çalıntı kopya kullandığı anlamına gelir. Gerçek kullanıcı da saldırgan da
  aynı zinciri kullanıyor olabileceğinden, o kullanıcının TÜM oturumları
  düşürülür. Yanlış pozitifi var (ağ tekrarı, çift sekme) ama güvenlik
  tarafında hata yapmak doğru yön.
"""

from __future__ import annotations

import hashlib
import os
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from api.db.models import RefreshToken


REFRESH_TOKEN_BYTES = 32
REFRESH_EXPIRE_DAYS = int(os.environ.get("CBT_REFRESH_EXPIRE_DAYS", "30"))

# İptal edilmiş satırlar bu süre boyunca duruyor. Silinirlerse rotate()
# çalıntı token'ı "bilinmeyen" sanar ve yeniden kullanım tespiti çalışmaz.
REUSE_DETECTION_DAYS = int(os.environ.get("CBT_REUSE_DETECTION_DAYS", "90"))
# İptal edilmiş token bu süre içinde tekrar gelirse yarış sayılıyor,
# saldırı değil. İki sekme aynı anda yenilediğinde ikincisi buraya düşer.
# Bedeli: çalıntı token'ı rotasyondan hemen sonra deneyen saldırgan
# tespitten kaçar. Dar bir pencere, karşılığında meşru kullanıcıyı
# tüm cihazlarından atmamak.
REUSE_GRACE_SECONDS = int(os.environ.get("CBT_REUSE_GRACE_SECONDS", "30"))


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _as_utc(dt: Optional[datetime]) -> Optional[datetime]:
    """SQLite tz bilgisini saklamıyor; karşılaştırma öncesi normalize et."""
    if dt is None:
        return None
    return dt if dt.tzinfo is not None else dt.replace(tzinfo=timezone.utc)


def hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def issue(
    db: Session,
    user_id: uuid.UUID,
    *,
    user_agent: Optional[str] = None,
    replaces: Optional[RefreshToken] = None,
) -> str:
    """Yeni refresh token üret, kaydı aç, ham değeri döndür.

    Ham değer yalnızca burada görülüyor — çağıran onu çereze koyacak.
    Veritabanına hash'i gidiyor.
    """
    raw = secrets.token_urlsafe(REFRESH_TOKEN_BYTES)
    row = RefreshToken(
        user_id=user_id,
        token_hash=hash_token(raw),
        expires_at=_now() + timedelta(days=REFRESH_EXPIRE_DAYS),
        user_agent=(user_agent or "")[:200] or None,
    )
    db.add(row)
    db.flush()

    if replaces is not None:
        replaces.revoked_at = _now()
        replaces.replaced_by = row.id

    return raw


def revoke_all_for_user(db: Session, user_id: uuid.UUID) -> int:
    """Kullanıcının açık tüm oturumlarını kapat. Kaç tanesinin kapandığını döner."""
    rows = db.execute(
        select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked_at.is_(None),
        )
    ).scalars().all()
    now = _now()
    for r in rows:
        r.revoked_at = now
    return len(rows)


class RefreshOutcome:
    """rotate() sonucu. Üç durumdan biri."""

    OK = "ok"                 # geçerli, yeni token verildi
    INVALID = "invalid"       # bilinmeyen ya da süresi dolmuş
    REUSE = "reuse"           # iptal edilmiş token tekrar kullanıldı
    RACE = "race"             # iptal edilmiş ama yeni kapanmış — yarış


def rotate(
    db: Session,
    raw_token: str,
    *,
    user_agent: Optional[str] = None,
) -> tuple[str, Optional[uuid.UUID], Optional[str]]:
    """Refresh token'ı doğrula ve döndür.

    Dönen üçlü: (sonuç, user_id, yeni_ham_token)

    REUSE durumunda kullanıcının tüm oturumları düşürülür ve yeni token
    verilmez — çağıran çerezi silip 401 dönmeli.
    """
    row = db.execute(
        select(RefreshToken).where(RefreshToken.token_hash == hash_token(raw_token))
    ).scalar_one_or_none()

    if row is None:
        return (RefreshOutcome.INVALID, None, None)

    if row.revoked_at is not None:
        yas = (_now() - _as_utc(row.revoked_at)).total_seconds()
        if yas <= REUSE_GRACE_SECONDS and row.replaced_by is not None:
            # Bu token az önce yenilendi ve yerine geçen kayıt var.
            # Muhtemelen ikinci bir sekme ya da tekrar gönderilmiş istek.
            # Oturumları düşürmüyoruz; istemci yeni çerezle tekrar denesin.
            return (RefreshOutcome.RACE, row.user_id, None)

        revoke_all_for_user(db, row.user_id)
        return (RefreshOutcome.REUSE, row.user_id, None)

    if _as_utc(row.expires_at) <= _now():
        return (RefreshOutcome.INVALID, row.user_id, None)

    row.last_used_at = _now()
    new_raw = issue(db, row.user_id, user_agent=user_agent, replaces=row)
    return (RefreshOutcome.OK, row.user_id, new_raw)


def revoke_one(db: Session, raw_token: str) -> bool:
    """Tek oturumu kapat (çıkış). Zaten kapalıysa ya da yoksa False."""
    row = db.execute(
        select(RefreshToken).where(RefreshToken.token_hash == hash_token(raw_token))
    ).scalar_one_or_none()
    if row is None or row.revoked_at is not None:
        return False
    row.revoked_at = _now()
    return True


def purge_expired(db: Session) -> int:
    """Artık hiçbir işe yaramayan kayıtları sil. Zamanlanmış temizlik için.

    İptal edilmiş satırlar hemen silinmiyor. rotate() bir token'ın daha önce
    kullanılıp kapatıldığını ancak satır durduğu sürece görebiliyor; satırı
    silersek çalıntı token "bilinmeyen" görünür, INVALID döner ve yeniden
    kullanım tespiti sessizce devre dışı kalır.

    Bu yüzden iki ayrı süre var:
      - hiç kullanılmadan süresi dolmuş satırlar: expires_at geçince gider
      - iptal edilmiş satırlar: tespit penceresi dolduktan sonra gider

    Açık (iptal edilmemiş, süresi dolmamış) satırlara dokunulmuyor.
    """
    now = _now()
    tespit_siniri = now - timedelta(days=REUSE_DETECTION_DAYS)

    rows = db.execute(select(RefreshToken)).scalars().all()

    silinen = 0
    for r in rows:
        revoked = _as_utc(r.revoked_at)
        expires = _as_utc(r.expires_at)

        if revoked is not None:
            # İptal edilmiş — tespit penceresi dolduysa sil
            if revoked < tespit_siniri:
                db.delete(r)
                silinen += 1
        elif expires is not None and expires <= now:
            # Hiç kullanılmadan süresi dolmuş — tespit değeri yok
            db.delete(r)
            silinen += 1

    return silinen
