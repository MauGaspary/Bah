from tests.helpers import request


def test_create_demo(client):
    response = request(
        client,
        "POST",
        "/demo/",
        json={"username": "testuser", "email": "test@example.com"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_get_demos(client):
    response = request(client, "GET", "/demo/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_demo_by_id(client, admin_global):
    response = request(client, "GET", f"/demo/id/{admin_global['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == admin_global["id"]


def test_get_demo_by_id_not_found(client):
    response = request(client, "GET", "/demo/id/9999")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Demo não encontrado"


def test_get_demo_by_email(client, admin_global):
    response = request(client, "GET", f"/demo/email/{admin_global['email']}")

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == admin_global["email"]


def test_get_demo_by_email_not_found(client):
    response = request(client, "GET", "/demo/email/nonexistent@example.com")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Demo não encontrado"


def test_create_demo_invalid_email(client):
    response = request(
        client,
        "POST",
        "/demo/",
        json={"username": "testuser", "email": "invalid-email"},
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Formato de email inválido"


def test_create_demo_duplicate_email(client, admin_global):
    response = request(
        client,
        "POST",
        "/demo/",
        json={"username": "newuser", "email": admin_global["email"]},
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Email já está em uso"
