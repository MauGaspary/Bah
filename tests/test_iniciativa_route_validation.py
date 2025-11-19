def test_search_requires_q(client):
    resp = client.get("/iniciativas/search", params={"page": 1, "size": 10})
    assert resp.status_code == 422
    assert any(err["loc"][-1] == "q" for err in resp.json()["detail"])


def test_search_rejects_page_lt_1(client):
    resp = client.get(
        "/iniciativas/search", params={"q": "teste", "page": 0, "size": 10}
    )
    assert resp.status_code == 422


def test_search_rejects_size_out_of_bounds(client):
    resp = client.get(
        "/iniciativas/search", params={"q": "teste", "page": 1, "size": 101}
    )
    assert resp.status_code == 422
