"""Direct unit tests on the DB-backed session store."""

import time

from api.session import DbSessionStore, _hash_message


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
