import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_empty_state():
    response = client.get("/admin/iniciativas")
    data = response.json()
    assert response.status_code == 200
    assert data["items"] == []
    assert data["total"] == 0


def test_filter_by_status(db_seed):
    response = client.get("/admin/iniciativas?status=ativa")
    data = response.json()
    assert all(item["status"] == "ativa" for item in data["items"])


def test_search_by_tag(db_seed):
    response = client.get("/admin/iniciativas?q=educacao")
    data = response.json()
    assert any("educacao" in tag for item in data["items"] for tag in item.get("tags", []))


def test_pagination(db_seed):
    r1 = client.get("/admin/iniciativas?page=1&size=2").json()
    r2 = client.get("/admin/iniciativas?page=2&size=2").json()
    ids_page1 = {i["id"] for i in r1["items"]}
    ids_page2 = {i["id"] for i in r2["items"]}
    assert ids_page1.isdisjoint(ids_page2)


def test_invalid_params():
    response = client.get("/admin/iniciativas?page=0")
    assert response.status_code == 422
