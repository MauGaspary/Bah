import pytest

from tests.helpers import request


@pytest.mark.integration
class TestAdminIntegration:
    """Testes de integração para o módulo Admin"""

    def test_create_and_retrieve_admin_flow(self, client):
        """Testa o fluxo completo de criação e recuperação de admin"""
        initial_response = request(client, "GET", "/admin/")
        assert initial_response.status_code == 200
        assert len(initial_response.json()) == 0

        admin_data = {"username": "admin_test", "email": "admin@test.com"}

        # 1. Criar admin
        create_response = request(client, "POST", "/admin/", json=admin_data)
        assert create_response.status_code == 200

        created_admin = create_response.json()
        assert created_admin["username"] == admin_data["username"]
        assert created_admin["email"] == admin_data["email"]
        assert "id" in created_admin
        assert "created_at" in created_admin

        # 2. Listar admins e verificar se o admin criado está na lista
        list_response = request(client, "GET", "/admin/")
        assert list_response.status_code == 200

        admins_list = list_response.json()
        assert len(admins_list) == 1
        assert admins_list[0]["id"] == created_admin["id"]
        assert admins_list[0]["username"] == admin_data["username"]

    def test_multiple_admins_creation(self, client):
        """Testa criação de múltiplos admins"""
        initial_response = request(client, "GET", "/admin/")
        assert initial_response.status_code == 200
        assert len(initial_response.json()) == 0

        admins_data = [
            {"username": "admin1", "email": "admin1@test.com"},
            {"username": "admin2", "email": "admin2@test.com"},
            {"username": "admin3", "email": "admin3@test.com"},
        ]

        created_ids = []

        # Criar múltiplos admins
        for admin_data in admins_data:
            response = request(client, "POST", "/admin/", json=admin_data)
            assert response.status_code == 200
            created_ids.append(response.json()["id"])

        # Verificar se todos foram criados
        list_response = request(client, "GET", "/admin/")
        assert list_response.status_code == 200

        admins_list = list_response.json()
        assert len(admins_list) == 3

        # Verificar se todos os IDs estão presentes
        returned_ids = [admin["id"] for admin in admins_list]
        assert set(created_ids) == set(returned_ids)

    def test_empty_admin_list(self, client):
        """Testa listagem quando não há admins"""
        response = request(client, "GET", "/admin/")
        assert response.status_code == 200
        assert response.json() == []

    def test_admin_data_validation(self, client):
        """Testa validação de dados do admin"""
        # Teste com email inválido
        invalid_data = {
            "username": "valid_user",
            "email": "invalid-email",  # email inválido
        }

        response = request(client, "POST", "/admin/", json=invalid_data)
        assert response.status_code == 400
        assert "Formato de email inválido" in response.json()["detail"]

    def test_admin_creation_with_special_characters(self, client):
        """Testa criação de admin com formatos válidos de email"""
        admin_data = {
            "username": "admin_test_123",
            "email": "admin+test@example.com",
        }

        response = request(client, "POST", "/admin/", json=admin_data)
        assert response.status_code == 200

        created_admin = response.json()
        assert created_admin["username"] == admin_data["username"]
        assert created_admin["email"] == admin_data["email"]

    def test_duplicate_email_validation(self, client):
        """Testa validação de email duplicado"""
        admin_data = {"username": "admin1", "email": "test@example.com"}

        # Criar primeiro admin
        response1 = request(client, "POST", "/admin/", json=admin_data)
        assert response1.status_code == 200

        # Tentar criar segundo admin com mesmo email
        admin_data2 = {"username": "admin2", "email": "test@example.com"}
        response2 = request(client, "POST", "/admin/", json=admin_data2)

        assert response2.status_code == 400
        assert "Email já está em uso" in response2.json()["detail"]

    def test_same_username_different_email_allowed(self, client):
        """Testa que usernames iguais são permitidos com emails diferentes"""
        admin_data1 = {"username": "admin_comum", "email": "test1@example.com"}
        admin_data2 = {"username": "admin_comum", "email": "test2@example.com"}

        # Criar primeiro admin
        response1 = request(client, "POST", "/admin/", json=admin_data1)
        assert response1.status_code == 200

        # Criar segundo admin com mesmo username mas email diferente
        response2 = request(client, "POST", "/admin/", json=admin_data2)
        assert response2.status_code == 200

        # Verificar que ambos foram criados
        created_admin1 = response1.json()
        created_admin2 = response2.json()

        assert created_admin1["username"] == created_admin2["username"]
        assert created_admin1["email"] != created_admin2["email"]
        assert created_admin1["id"] != created_admin2["id"]

    def test_invalid_email_format_validation(self, client):
        """Testa validação de formato de email inválido"""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "user@",
            "user.example.com",
            "user@.com",
        ]

        for invalid_email in invalid_emails:
            admin_data = {"username": "test", "email": invalid_email}
            response = request(client, "POST", "/admin/", json=admin_data)

            assert response.status_code == 400
            assert "Formato de email inválido" in response.json()["detail"]
