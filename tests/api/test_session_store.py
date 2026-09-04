"""Direct unit tests on the DB-backed session store."""

import time
import uuid
from datetime import timedelta

from api.session import DbSessionStore, _hash_message, _now


def test_new_session_creates_uuid(app):
    s = DbSessionStore()
    sid = s.new_session()
    assert sid
    assert len(sid) == 36  # uuid4


def test_append_turn_and_read(app):
    s = DbSessionStore()
    sid = s.new_session()
    tid = s.append_turn(sid, "user says hi", "assistant says hi",
                        "cbt_support", "unknown")
    sess = s.get_session(sid)
    assert sess["turns"][0]["turn_id"] == tid
    assert sess["turns"][0]["user_message"] == "user says hi"
    assert sess["turns"][0]["user_hash"] == _hash_message("user says hi")


def test_get_history(app):
    s = DbSessionStore()
    sid = s.new_session()
    s.append_turn(sid, "msg1", "resp1", "cbt_support", "unknown")
    s.append_turn(sid, "msg2", "resp2", "cbt_support", "unknown")
    hist = s.get_history(sid)
    assert len(hist) == 2
    assert hist[0] == {"user_message": "msg1", "response": "resp1"}
    assert hist[1] == {"user_message": "msg2", "response": "resp2"}
    # Unknown session returns []
    assert s.get_history("00000000-0000-0000-0000-000000000000") == []


def test_ensure_reuses_existing(app):
    s = DbSessionStore()
    sid = s.new_session()
    same = s.ensure(sid)
    assert same == sid
    fresh = s.ensure(None)
    assert fresh != sid


def test_delete(app):
    s = DbSessionStore()
    sid = s.new_session()
    assert s.delete(sid) is True
    assert s.delete(sid) is False
    assert s.get_session(sid) is None


def test_ttl_gc(app):
    s = DbSessionStore(ttl_seconds=0)
    sid = s.new_session()
    time.sleep(0.01)
    # Any append triggers gc
    s.append_turn(s.new_session(), "hi", "hi back", "cbt_support", "unknown")
    assert s.get_session(sid) is None


def test_ttl_gc_keeps_user_sessions(app):
    """Kayıtlı kullanıcının oturumu TTL dolsa da silinmemeli."""
    import uuid as _uuid
    from api import db as _db
    from api.db.models import User

    s = DbSessionStore(ttl_seconds=0)

    with _db.get_sessionmaker()() as sess, sess.begin():
        user = User(
            email=f"gc-{_uuid.uuid4().hex[:8]}@test.com",
            password_hash="x",
            email_verified=True,
        )
        sess.add(user)
        sess.flush()
        uid = user.id

    anon_sid = s.new_session()
    user_sid = s.new_session()
    s.attach_user(user_sid, uid)

    time.sleep(0.01)
    s.append_turn(s.new_session(), "hi", "hi back", "cbt_support", "unknown")

    assert s.get_session(anon_sid) is None
    assert s.get_session(user_sid) is not None


def test_user_turns_have_no_retention_deadline(app):
    """Anonim turda retention_ends_at dolu, kayıtlı kullanıcıda boş olmalı."""
    import uuid as _uuid
    from api import db as _db
    from api.db.models import User, Turn

    s = DbSessionStore()

    with _db.get_sessionmaker()() as sess, sess.begin():
        user = User(
            email=f"ret-{_uuid.uuid4().hex[:8]}@test.com",
            password_hash="x",
            email_verified=True,
        )
        sess.add(user)
        sess.flush()
        uid = user.id

    anon_sid = s.new_session()
    anon_tid = s.append_turn(anon_sid, "hi", "cevap", "cbt_support", "unknown")

    user_sid = s.new_session()
    s.attach_user(user_sid, uid)
    user_tid = s.append_turn(user_sid, "hi", "cevap", "cbt_support", "unknown")

    with _db.get_sessionmaker()() as sess:
        assert sess.get(Turn, _uuid.UUID(anon_tid)).retention_ends_at is not None
        assert sess.get(Turn, _uuid.UUID(user_tid)).retention_ends_at is None


# ============================================================
# sitting_turn_count — seans yayı oturuma değil, oturuşa bağlı
# ============================================================

def _backdate_turn(turn_id: str, delta: timedelta) -> None:
    """Bir turun zaman damgasını geriye al — uzun ara simülasyonu."""
    from api import db as _db
    from api.db.models import Turn

    with _db.get_sessionmaker()() as s, s.begin():
        row = s.get(Turn, uuid.UUID(turn_id))
        row.ts = _now() - delta


def test_sitting_count_empty_session(app):
    s = DbSessionStore()
    assert s.sitting_turn_count(s.new_session()) == 0


def test_sitting_count_invalid_id(app):
    s = DbSessionStore()
    assert s.sitting_turn_count("not-a-uuid") == 0


def test_sitting_count_counts_consecutive_turns(app):
    s = DbSessionStore()
    sid = s.new_session()
    for _ in range(3):
        s.append_turn(sid, "mesaj", "cevap", "cbt_support", "unknown")
    assert s.sitting_turn_count(sid) == 3


def test_sitting_count_resets_after_long_gap(app):
    """Son turun üzerinden uzun süre geçtiyse sıradaki mesaj yeni oturuş açar."""
    s = DbSessionStore()
    sid = s.new_session()
    for _ in range(5):
        tid = s.append_turn(sid, "mesaj", "cevap", "cbt_support", "unknown")

    assert s.sitting_turn_count(sid) == 5

    # Bütün turları 3 gün geriye al
    from api import db as _db
    from api.db.models import Turn
    from sqlalchemy import select as _select

    with _db.get_sessionmaker()() as db, db.begin():
        rows = db.execute(
            _select(Turn).where(Turn.session_id == uuid.UUID(sid))
        ).scalars().all()
        for r in rows:
            r.ts = _now() - timedelta(days=3)

    assert s.sitting_turn_count(sid) == 0


def test_sitting_count_gap_inside_session(app):
    """Ortada uzun ara varsa sayaç aradan sonrasını sayar."""
    s = DbSessionStore()
    sid = s.new_session()

    old_ids = [s.append_turn(sid, "eski", "cevap", "cbt_support", "unknown") for _ in range(4)]
    for tid in old_ids:
        _backdate_turn(tid, timedelta(days=2))

    for _ in range(2):
        s.append_turn(sid, "yeni", "cevap", "cbt_support", "unknown")

    assert s.sitting_turn_count(sid) == 2


def test_sitting_count_short_break_stays_same_sitting(app):
    """Kısa ara (varsayılan eşiğin altı) oturuşu bölmemeli."""
    s = DbSessionStore()
    sid = s.new_session()

    tid = s.append_turn(sid, "mesaj", "cevap", "cbt_support", "unknown")
    _backdate_turn(tid, timedelta(hours=2))
    s.append_turn(sid, "mesaj", "cevap", "cbt_support", "unknown")

    assert s.sitting_turn_count(sid) == 2


def test_get_history_respects_limit(app):
    """Uzun oturumda geçmiş sınırlanmalı ve son turlar dönmeli."""
    s = DbSessionStore()
    sid = s.new_session()
    for i in range(8):
        s.append_turn(sid, f"mesaj-{i}", f"cevap-{i}", "cbt_support", "unknown")

    hist = s.get_history(sid, limit=3)
    assert len(hist) == 3
    assert [h["user_message"] for h in hist] == ["mesaj-5", "mesaj-6", "mesaj-7"]
