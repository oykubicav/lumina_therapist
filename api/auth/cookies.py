"""Refresh token çerezi — kurma, okuma, silme ve CSRF başlık kontrolü.

Çerez neden httpOnly: refresh token uzun ömürlü ve iptal edilebilir tek
kimlik bilgisi. JavaScript'in okuyabildiği bir yerde durursa XSS ile
çalınabilir ve saldırgan süresiz access token üretir. httpOnly çerezi
JavaScript göremiyor.

Neden Path=/auth: çerez yalnızca /auth/refresh ve /auth/logout tarafından
kullanılıyor. /chat'e her mesajda gitmesine gerek yok.

Neden Domain yok: Domain koymazsak çerez host-only oluyor, sadece
api.askneva.com'a gidiyor. Domain=.askneva.com yazsaydık askneva.com'a da
giderdi — gereksiz genişleme.
"""

from __future__ import annotations

import os
from typing import Optional

from fastapi import HTTPException, Request, Response, status

from api.auth.refresh_tokens import REFRESH_EXPIRE_DAYS


REFRESH_COOKIE_NAME = "cbt_refresh"
REFRESH_COOKIE_PATH = "/auth"

# Üretimde her zaman Secure. Yerel geliştirmede http kullanıldığı için
# .env'de 0'a çekiliyor. Varsayılanın güvenli taraf olması bilinçli:
# unutulursa üretim korunmuş olur.
COOKIE_SECURE = os.environ.get("CBT_COOKIE_SECURE", "1") == "1"

# Tarayıcının basit form POST'uyla gönderemediği bir başlık. Varlığı CORS
# ön kontrolünü zorunlu kılıyor, ön kontrolü de CORS ayarı reddediyor.
# SameSite=Lax üstüne ikinci bir CSRF katmanı.
CLIENT_HEADER = "x-neva-client"


def set_refresh_cookie(response: Response, raw_token: str) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=raw_token,
        max_age=REFRESH_EXPIRE_DAYS * 24 * 3600,
        path=REFRESH_COOKIE_PATH,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
    )


def clear_refresh_cookie(response: Response) -> None:
    # Silmek için aynı path ve bayraklarla boş değer yazılıyor; path
    # eşleşmezse tarayıcı eski çerezi bırakır.
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path=REFRESH_COOKIE_PATH,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
    )


def get_refresh_cookie(request: Request) -> Optional[str]:
    return request.cookies.get(REFRESH_COOKIE_NAME)


def require_client_header(request: Request) -> None:
    """CSRF ikinci katmanı. Çerez taşıyan uçlarda Depends ile kullanılıyor."""
    if request.headers.get(CLIENT_HEADER) is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Eksik istemci başlığı",
        )