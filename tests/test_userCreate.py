from datetime import date, time

import pytest

from tests.helpers import request, request_auth


@pytest.mark.integration
class TestUserCreationIntegration:

    def test_create_user_success(self, client):
        user_data = {
            "nome": "Teste",
            "sobrenome": "Usuario",
            "email": "teste@gmail.com",
            "password": "senha123",
        }

        response = request(client, "POST", "/users/", json=user_data)

        assert response.status_code == 200

        created_user = response.json()
        assert created_user["nome"] == user_data["nome"]
        assert created_user["sobrenome"] == user_data["sobrenome"]
        assert created_user["email"] == user_data["email"]
        assert "id" in created_user
        assert "criado_em" in created_user
        assert "password" not in created_user
        assert "senha_hash" not in created_user

    def test_create_user_invalid_email(self, client):
        user_data = {
            "nome": "Teste",
            "sobrenome": "Usuario",
            "email": "email-invalido",
            "password": "senha123",
        }

        response = request(client, "POST", "/users/", json=user_data)

        assert response.status_code == 422
        error_detail = response.json()["detail"]
        assert "email" in str(error_detail).lower()

    def test_create_user_duplicate_email(self, client):
        user_data1 = {
            "nome": "Teste1",
            "sobrenome": "Usuario1",
            "email": "teste@gmail.com",
            "password": "senha123",
        }

        user_data2 = {
            "nome": "Teste2",
            "sobrenome": "Usuario2",
            "email": "teste@gmail.com",
            "password": "senha123",
        }

        response1 = request(client, "POST", "/users/", json=user_data1)
        assert response1.status_code == 200

        response2 = request(client, "POST", "/users/", json=user_data2)

        assert response2.status_code == 400
        assert "Email já está em uso" in response2.json()["detail"]

    def test_create_user_missing_fields(self, client):
        user_data_no_nome = {
            "sobrenome": "Usuario",
            "email": "teste@gmail.com",
            "password": "senha123",
        }

        response = request(client, "POST", "/users/", json=user_data_no_nome)
        assert response.status_code == 422
        error_detail = response.json()["detail"]
        assert "nome" in str(error_detail).lower()

        user_data_no_sobrenome = {
            "nome": "Teste",
            "email": "teste@gmail.com",
            "password": "senha123",
        }

        response = request(client, "POST", "/users/", json=user_data_no_sobrenome)
        assert response.status_code == 422
        error_detail = response.json()["detail"]
        assert "sobrenome" in str(error_detail).lower()

        user_data_no_email = {
            "nome": "Teste",
            "sobrenome": "Usuario",
            "password": "senha123",
        }

        response = request(client, "POST", "/users/", json=user_data_no_email)
        assert response.status_code == 422
        error_detail = response.json()["detail"]
        assert "email" in str(error_detail).lower()

        user_data_no_password = {
            "nome": "Teste",
            "sobrenome": "Usuario",
            "email": "teste@gmail.com",
        }

        response = request(client, "POST", "/users/", json=user_data_no_password)
        assert response.status_code == 422
        error_detail = response.json()["detail"]
        assert "password" in str(error_detail).lower()

    def test_create_user_empty_fields(self, client):
        user_data_empty_nome = {
            "nome": "",
            "sobrenome": "Usuario",
            "email": "teste@gmail.com",
            "password": "senha123",
        }

        response = request(client, "POST", "/users/", json=user_data_empty_nome)
        assert response.status_code == 422
        error_detail = response.json()["detail"]
        assert "nome" in str(error_detail).lower()

        user_data_empty_sobrenome = {
            "nome": "Teste",
            "sobrenome": "",
            "email": "teste@gmail.com",
            "password": "senha123",
        }
        response = request(client, "POST", "/users/", json=user_data_empty_sobrenome)
        assert response.status_code == 422
        error_detail = response.json()["detail"]
        assert "sobrenome" in str(error_detail).lower()

        user_data_empty_email = {
            "nome": "Teste",
            "sobrenome": "Usuario",
            "email": "",
            "password": "senha123",
        }
        response = request(client, "POST", "/users/", json=user_data_empty_email)
        assert response.status_code == 422
        error_detail = response.json()["detail"]
        assert "email" in str(error_detail).lower()

        user_data_empty_password = {
            "nome": "Teste",
            "sobrenome": "Usuario",
            "email": "teste@gmail.com",
            "password": "",
        }
        response = request(client, "POST", "/users/", json=user_data_empty_password)
        assert response.status_code == 422
        error_detail = response.json()["detail"]
        assert "password" in str(error_detail).lower()
