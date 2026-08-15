"""POST /consent tests."""


def test_consent_new_session(client):
    r = client.post("/consent", json={"policy_version": "0.2"})
    assert r.status_code == 200
    body = r.json()
    assert body["session_id"]
    assert body["consent_id"]
    assert body["policy_version"] == "0.2"


def test_consent_existing_session(client):
    r1 = client.post("/consent", json={"policy_version": "0.2"})
    sid = r1.json()["session_id"]
    r2 = client.post("/consent", json={
        "policy_version": "0.2",
        "session_id": sid,
    })
    assert r2.status_code == 200
    assert r2.json()["session_id"] == sid
    # New consent record even for same session (versioning trail)
    assert r2.json()["consent_id"] != r1.json()["consent_id"]


def test_consent_wrong_policy_version(client):
    r = client.post("/consent", json={"policy_version": "0.0-old"})
    assert r.status_code == 400
