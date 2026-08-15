"""POST /chat endpoint tests using mock LLM provider."""

import pytest


def test_chat_low_risk_message(client):
    r = client.post("/chat", json={
        "user_message": "Sürekli nabzımı kontrol ediyorum, kalbim hızlı atıyor.",
        "options": {"enable_llm_critic": False},
    })
    assert r.status_code == 200
    body = r.json()
    assert body["session_id"]
    assert body["turn_id"]
    assert body["safety"]["route"] == "cbt_support"
    assert body["safety"]["allow_cbt"] is True


def test_chat_safety_hard_stop(client):
    r = client.post("/chat", json={
        "user_message": "Ölmek istiyorum, kendime zarar vermeyi düşünüyorum.",
        "options": {"enable_llm_critic": False},
    })
    assert r.status_code == 200
    body = r.json()
    assert body["safety"]["allow_cbt"] is False
    assert body["safety"]["route"] == "crisis_referral"
    assert "safety_self_harm_suicide_001" in body["safety"]["matched_card_ids"]
    # Mock safety response must contain 112 + uzman
    assert "112" in body["response"]


def test_chat_reuses_session_id(client):
    r1 = client.post("/chat", json={"user_message": "Merhaba."})
    sid = r1.json()["session_id"]
    r2 = client.post("/chat", json={"user_message": "Devam edelim.", "session_id": sid})
    assert r2.json()["session_id"] == sid


def test_chat_empty_message_rejected(client):
    r = client.post("/chat", json={"user_message": ""})
    assert r.status_code == 422


def test_chat_too_long_message_rejected(client):
    r = client.post("/chat", json={"user_message": "x" * 4001})
    assert r.status_code == 422


def test_delete_session(client):
    r1 = client.post("/chat", json={"user_message": "Merhaba."})
    sid = r1.json()["session_id"]
    r2 = client.delete(f"/chat/session/{sid}")
    assert r2.status_code == 200
    assert r2.json()["deleted"] is True
