"""GET /cards endpoint tests."""


def test_list_cards(client):
    r = client.get("/cards")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] >= 50
    assert len(body["cards"]) == 20  # default limit


def test_filter_by_topic(client):
    r = client.get("/cards?topic=panic")
    body = r.json()
    assert all(c["topic"] == "panic" for c in body["cards"])
    assert body["total"] == 10


def test_filter_by_type(client):
    r = client.get("/cards?type=exercise")
    body = r.json()
    assert all(c["type"] == "exercise" for c in body["cards"])


def test_search_by_title(client):
    r = client.get("/cards?q=döngü")
    body = r.json()
    assert body["total"] >= 1
    assert all("döngü" in c["title_tr"].lower() for c in body["cards"])


def test_pagination(client):
    r1 = client.get("/cards?limit=5&offset=0")
    r2 = client.get("/cards?limit=5&offset=5")
    ids1 = {c["id"] for c in r1.json()["cards"]}
    ids2 = {c["id"] for c in r2.json()["cards"]}
    assert not (ids1 & ids2)


def test_get_single_card(client):
    r = client.get("/cards/pa_grounding_004")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == "pa_grounding_004"
    assert body["topic"] == "panic"
    assert body["content_tr"]


def test_get_nonexistent_card(client):
    r = client.get("/cards/does_not_exist_001")
    assert r.status_code == 404


def test_topics(client):
    r = client.get("/cards/topics")
    body = r.json()
    topics = body["topics"]
    assert len(topics) >= 5
    ids = {t["topic"] for t in topics}
    assert {"panic", "depression", "gad"} <= ids
    for t in topics:
        assert t["count"] > 0
        assert t["display_name_tr"]


def test_safety_cards_list(client):
    # Admin gate is open when CBT_ADMIN_TOKEN is unset
    r = client.get("/cards/safety")
    body = r.json()
    assert body["total"] >= 10
    ids = {c["card_id"] for c in body["cards"]}
    assert "safety_self_harm_suicide_001" in ids
    for card in body["cards"]:
        assert card["card_id"]
        assert card["safe_response_template_tr"]
