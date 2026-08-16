"""Şifre hash'leme — bcrypt.

passlib kullanılmıyor: passlib 1.7.4 başlatılırken 72 byte'tan uzun bir test
parolası deniyor, bcrypt 4.1+ bunu ValueError ile reddediyor. Doğrudan bcrypt
aynı hash formatını ($2b$...) üretir, mevcut hash'ler geçerli kalır.
"""

import bcrypt

# bcrypt'in kendi sınırı: parola 72 byte'ı geçemez.
_MAX_BYTES = 72


def _to_bytes(plain: str) -> bytes:
    return plain.encode("utf-8")[:_MAX_BYTES]


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(_to_bytes(plain), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(_to_bytes(plain), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False
