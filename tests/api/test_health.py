"""Health + readiness endpoint tests."""


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert "version" in body


def test_readyz(client):
    r = client.get("/readyz")
    assert r.status_code == 200
    body = r.json()
    # Cards + rules should be loadable in test env
    assert body["checks"]["cbt_cards"] is True
    assert body["checks"]["safety_cards"] is True
    assert body["checks"]["safety_rules"] is True
    assert body["checks"]["embedding_backend"] is True


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "CBT API" in r.json()["message"]
