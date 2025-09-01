"""Exemplo de uso dos helpers de teste"""

from tests.helpers import request, request_auth


class TestHelpersUsage:
    """Exemplos de como usar os helpers nos testes"""

    def test_basic_request(self, client):
        """Exemplo básico usando helper request"""
        response = request(client, "GET", "/admin/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_post_request(self, client):
        """Exemplo de POST usando helper request"""
        response = request(
            client,
            "POST",
            "/admin/",
            json={"username": "example", "email": "example@test.com"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "example"
        assert data["email"] == "example@test.com"

    def test_auth_request_example(self, client):
        """Exemplo de request autenticado (endpoint fictício)"""
        fake_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.fake.token"

        # Este endpoint não existe, mas demonstra o uso
        response = request_auth(client, "GET", "/admin/protected", token=fake_token)

        # Esperamos 404 pois o endpoint não existe
        assert response.status_code == 404

    def test_custom_headers(self, client):
        """Exemplo com headers customizados"""
        response = request(
            client,
            "POST",
            "/admin/",
            json={"username": "custom", "email": "custom@test.com"},
            headers={"X-Test-Header": "test-value"},
        )

        assert response.status_code == 200
