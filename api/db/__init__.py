"""Database layer — SQLAlchemy 2.0 engine + session dependency.

Design:
- Engine + sessionmaker are module-level singletons keyed to the DB URL.
- URL comes from env var CBT_DB_URL (defaults to local Postgres).
- Tests override CBT_DB_URL to sqlite:///:memory: (via conftest fixture).
- get_db() yields a Session for FastAPI Depends injection.
- init_engine() is called by main.py at startup to fail fast on bad config.

KVKK note: this module never logs raw user_message. Persistence choices
(which columns nullable, retention policy) live in models.py + session.py.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from functools import lru_cache
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


# ============================================================
# URL resolution
# ============================================================

def _default_db_url() -> str:
    """Compose default DB URL from parts, or full override via CBT_DB_URL.

    Render/Heroku Postgres connectionString uses `postgresql://` scheme,
    which SQLAlchemy defaults to psycopg2. Biz psycopg (v3) kullanıyoruz —
    URL'i normalize et.
    """
    url = os.environ.get("CBT_DB_URL")
    if url:
        # Auto-upgrade to psycopg v3 driver
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        elif url.startswith("postgres://"):
            # Heroku/Render legacy scheme
            url = url.replace("postgres://", "postgresql+psycopg://", 1)
        return url
    # Postgres default — matches docker-compose service
    user = os.environ.get("CBT_DB_USER", "cbt")
    pw = os.environ.get("CBT_DB_PASSWORD", "cbt")
    host = os.environ.get("CBT_DB_HOST", "localhost")
    port = os.environ.get("CBT_DB_PORT", "5432")
    name = os.environ.get("CBT_DB_NAME", "cbt")
    return f"postgresql+psycopg://{user}:{pw}@{host}:{port}/{name}"


def get_db_url() -> str:
    return _default_db_url()


# ============================================================
# Engine + session factory
# ============================================================

_engine: Engine | None = None
_SessionLocal: sessionmaker | None = None


def _make_engine(url: str) -> Engine:
    """Create an SQLAlchemy engine tuned to the driver in the URL."""
    connect_args = {}
    engine_kwargs = {
        "pool_pre_ping": True,
        "future": True,
    }
    if url.startswith("sqlite"):
        # Tests: single-connection in-memory SQLite needs StaticPool so
        # every session sees the same schema.
        from sqlalchemy.pool import StaticPool
        connect_args["check_same_thread"] = False
        engine_kwargs["poolclass"] = StaticPool
    else:
        engine_kwargs["pool_size"] = 5
        engine_kwargs["max_overflow"] = 10
        engine_kwargs["pool_recycle"] = 300
    return create_engine(url, connect_args=connect_args, **engine_kwargs)


def init_engine(url: str | None = None) -> Engine:
    """Initialize the engine + sessionmaker singletons.

    Idempotent: if the URL hasn't changed, returns the existing engine.
    This matters for tests using in-memory SQLite + StaticPool — a fresh
    engine would drop the schema. Explicit reset_engine() is available if
    you need to force recreation.
    """
    global _engine, _SessionLocal
    resolved = url or get_db_url()
    if _engine is not None and str(_engine.url) == resolved:
        return _engine
    _engine = _make_engine(resolved)
    _SessionLocal = sessionmaker(bind=_engine, autoflush=False, expire_on_commit=False)
    return _engine


def reset_engine() -> None:
    """Test helper — drop the engine so init_engine() rebuilds it."""
    global _engine, _SessionLocal
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _SessionLocal = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        init_engine()
    assert _engine is not None
    return _engine


def get_sessionmaker() -> sessionmaker:
    global _SessionLocal
    if _SessionLocal is None:
        init_engine()
    assert _SessionLocal is not None
    return _SessionLocal


# ============================================================
# FastAPI dependency + context helper
# ============================================================

def get_db() -> Iterator[Session]:
    """FastAPI dependency — yields a Session, closes on exit."""
    SessionLocal = get_sessionmaker()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session() -> Iterator[Session]:
    """Context-manager variant for scripts / background tasks."""
    SessionLocal = get_sessionmaker()
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ============================================================
# Test helper — create schema without Alembic
# ============================================================

def create_all_for_tests() -> None:
    """Create all tables directly from models. Test-only convenience.
    Prod uses Alembic migrations."""
    from api.db.models import Base
    Base.metadata.create_all(bind=get_engine())


def drop_all_for_tests() -> None:
    from api.db.models import Base
    Base.metadata.drop_all(bind=get_engine())
