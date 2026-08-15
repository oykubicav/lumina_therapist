"""JWT token — encode/decode with HS256.

Token payload: {sub: user_id, exp: expiry}
Secret ve config env variable'lardan.
"""
import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import uuid

from jose import jwt, JWTError

_JWT_SECRET = os.environ.get("CBT_JWT_SECRET")
_JWT_ALGORITHM = os.environ.get("CBT_JWT_ALGORITHM", "HS256")
_JWT_EXPIRE_HOURS = int(os.environ.get("CBT_JWT_EXPIRE_HOURS", "168"))

if not _JWT_SECRET or len(_JWT_SECRET) < 32:
    raise RuntimeError(
        "CBT_JWT_SECRET env variable eksik ya da 32 karakterden kısa. "
        ".env'e ekle: CBT_JWT_SECRET=<random 32+ char string>"
    )

def encode_token(user_id: uuid.UUID, expire_hours: Optional[int] = None) -> str:
    """User ID → JWT string. Expire 1 hafta default."""
    hours = expire_hours or _JWT_EXPIRE_HOURS
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=hours),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, _JWT_SECRET, algorithm=_JWT_ALGORITHM)

def decode_token(token: str) -> Optional[uuid.UUID]:
    try:
        payload = jwt.decode(token, _JWT_SECRET, algorithms=[_JWT_ALGORITHM])
        sub = payload.get("sub")
        if not sub:
            return None
        return uuid.UUID(sub)
    except(JWTError,ValueError):
        return None


