"""POST /feedback tests."""

import uuid


def _create_turn(client):
    """Helper: send a chat message, return (session_id, turn_id)."""
    r = client.post("/chat", json={
        "user_message": "test message",
        "options": {"enable_llm_critic": False},
    })
    body = r.json()
    return body["session_id"], body["turn_id"]


def test_submit_feedback(client):
    sid, tid = _create_turn(client)
    r = client.post("/feedback", json={
        "turn_id": tid,
        "session_id": sid,
        "verdict": "thumbs_up",
        "comment": "İyi cevaptı",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["received"] is True
    assert body["feedback_id"]


def test_feedback_invalid_verdict(client):
    _, tid = _create_turn(client)
    r = client.post("/feedback", json={
        "turn_id": tid,
        "verdict": "invalid_verdict",
    })
    assert r.status_code == 422


def test_feedback_comment_too_long(client):
    _, tid = _create_turn(client)
    r = client.post("/feedback", json={
        "turn_id": tid,
        "verdict": "thumbs_down",
        "comment": "x" * 1001,
    })
    assert r.status_code == 422


def test_feedback_bad_uuid(client):
    r = client.post("/feedback", json={
        "turn_id": "not-a-uuid",
        "verdict": "thumbs_up",
    })
    assert r.status_code == 400
