import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(scope="session")
def admin_global():
    """Fixture que cria um admin global para usar em vários testes"""
    admin_data = {"username": "test_admin", "email": "test_admin@example.com"}
    response = client.post("/admin/", json=admin_data)
    return response.json()


def test_create_admin():
    admin_data = {"username": "testuser", "email": "test@example.com"}

    response = client.post("/admin/", json=admin_data)

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_get_admins():
    response = client.get("/admin/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_admin_by_id(admin_global):
    response = client.get(f"/admin/id/{admin_global['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == admin_global["id"]


def test_get_admin_by_id_not_found():
    """Busca de admin com ID que nao existe"""
    response = client.get("/admin/id/9999")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Admin não encontrado"


def test_get_admin_by_email(admin_global):
    response = client.get(f"/admin/email/{admin_global['email']}")

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == admin_global["email"]


def test_get_admin_by_email_not_found():
    """Busca de admin com email que nao existe"""
    response = client.get("/admin/email/nonexistent@example.com")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Admin não encontrado"
