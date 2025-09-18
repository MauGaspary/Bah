from tests.helpers import request

VALID_USER = {"email": "teste@gmail.com", "password": "senha123"}


def get_valid_token(test_user, client):
    response = request(client, "POST", "/auth/login", json=VALID_USER)
    assert response.status_code == 200
    return response.json()["access_token"]


class TestAuthMiddleware:

    def test_demo_endpoint_bypasses_middleware(self, client):
        response = request(client, "GET", "/demo/")
        assert response.status_code == 200

    def test_auth_endpoint_bypasses_middleware(self, client, test_user):
        response = request(client, "POST", "/auth/login", json=VALID_USER)
        assert response.status_code == 200

    def test_admin_endpoint_without_token(self, client):
        response = request(client, "GET", "/admin/iniciativas")
        assert response.status_code == 401
        assert response.json()["detail"] == "Authorization header required"

    def test_admin_endpoint_invalid_header_format(self, client):
        response = request(
            client,
            "GET",
            "/admin/iniciativas",
            headers={"Authorization": "InvalidFormat"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Authorization header required"

    def test_admin_endpoint_empty_token(self, client):
        response = request(
            client, "GET", "/admin/iniciativas", headers={"Authorization": "Bearer "}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Token required"

    def test_admin_endpoint_whitespace_token(self, client):
        response = request(
            client, "GET", "/admin/iniciativas", headers={"Authorization": "Bearer    "}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Token required"

    def test_admin_endpoint_invalid_token(self, client):
        response = request(
            client,
            "GET",
            "/admin/iniciativas",
            headers={"Authorization": "Bearer invalid_token"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid token"

    def test_admin_endpoint_valid_token(self, client, test_user):
        token = get_valid_token(test_user, client)
        response = request(
            client,
            "GET",
            "/admin/iniciativas",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code != 401
