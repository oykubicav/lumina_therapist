# api/deps.py
"""Dependency injection helpers for FastAPI routes.

Use with Depends(...) in route signatures. Keeps handlers testable and
env-config decoupled from routing.
"""

import os
from functools import lru_cache

from fastapi import Header, HTTPException, Request

from api.session import InMemorySessionStore, get_store as _get_store


# ============================================================
# Session store DI
# ============================================================

def session_store_dep() -> InMemorySessionStore:
    return _get_store()


# ============================================================
# API key auth (optional; used by admin routes if desired)
# ============================================================

EXPECTED_API_KEY = os.environ.get("MY_SECRET_API_KEY", "varsayilan_guvensiz_sifre")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != EXPECTED_API_KEY:
        raise HTTPException(status_code=403, detail="Yasak!")
    return x_api_key


# ============================================================
# Rate limiter (slowapi, optional)
# ============================================================

def _client_key(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@lru_cache(maxsize=1)
def _get_limiter():
    try:
        from slowapi import Limiter
    except ImportError:
        return None
    return Limiter(key_func=_client_key)


def limiter():
    return _get_limiter()


# ============================================================
# Admin gate (used by /cards/safety, /eval)
# ============================================================

def require_admin(request: Request) -> None:
    """Simple bearer-token admin guard.

    Set CBT_ADMIN_TOKEN in env; clients send `Authorization: Bearer <token>`.
    If CBT_ADMIN_TOKEN is unset, admin routes are OPEN (dev mode) — you
    must set it before deploying.
    """
    token = os.environ.get("CBT_ADMIN_TOKEN")
    if not token:
        return  # dev-open
    got = request.headers.get("authorization", "")
    if not got.startswith("Bearer ") or got.split(" ", 1)[1] != token:
        raise HTTPException(status_code=403, detail="admin token required")