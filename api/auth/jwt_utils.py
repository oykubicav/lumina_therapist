"""JWT token — encode/decode with HS256.

Token payload: {sub: user_id, exp: expiry}
Secret ve config env variable'lardan.

Secret doğrulaması import anında değil, ilk kullanımda yapılır: JWT'ye
dokunmayan uçlar (health, cards, chat) secret olmadan da çalışabilmeli.
Eksik secret'ın erken yakalanması için main.py startup'ta uyarı basar.
"""
import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import uuid

from jose import jwt, JWTError

_JWT_ALGORITHM = os.environ.get("CBT_JWT_ALGORITHM", "HS256")
# 72 saat. Ruh sağlığı verisi taşıyan bir oturum için 7 gün uzun; ama çok
# kısa tutmak da "kötü hissettiğimde açayım" kullanımını bozuyor, insanlar
# günler arayla giriyor. İptal edilebilirlik için refresh token gerekiyor,
# o ayrı bir iş.
_ACCESS_EXPIRE_MINUTES = int(os.environ.get("CBT_ACCESS_EXPIRE_MINUTES", "15"))

_MIN_SECRET_LEN = 32


def secret_is_configured() -> bool:
    secret = os.environ.get("CBT_JWT_SECRET")
    return bool(secret) and len(secret) >= _MIN_SECRET_LEN


def _get_secret() -> str:
    secret = os.environ.get("CBT_JWT_SECRET")
    if not secret or len(secret) < _MIN_SECRET_LEN:
        raise RuntimeError(
            "CBT_JWT_SECRET env variable eksik ya da 32 karakterden kısa. "
            ".env'e ekle: CBT_JWT_SECRET=<random 32+ char string>"
        )
    return secret


def encode_token(user_id: uuid.UUID, expire_minutes: Optional[int] = None) -> str:
    """User ID → kısa ömürlü access token."""
    minutes = expire_minutes or _ACCESS_EXPIRE_MINUTES
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=minutes),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, _get_secret(), algorithm=_JWT_ALGORITHM)


def decode_token(token: str) -> Optional[uuid.UUID]:
    try:
        payload = jwt.decode(token, _get_secret(), algorithms=[_JWT_ALGORITHM])
        sub = payload.get("sub")
        if not sub:
            return None
        return uuid.UUID(sub)
    except (JWTError, ValueError, RuntimeError):
        return None
