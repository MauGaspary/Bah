import uuid

import pytest

from app.models.organizador_model import Organizador
from tests.helpers import request, request_auth


class TestListarOrganizadores:
    """Testes para o endpoint GET /organizadores/"""

    def test_listar_organizadores_success(self, client, db_session, auth_token):
        """
        Happy Path: Lista organizadores com sucesso
        Given: Existem organizadores cadastrados no banco
        When: Faço uma requisição GET para /admin/organizadores/
        Then: Recebo status 200 e a lista de organizadores
        """
        org1 = Organizador(id=str(uuid.uuid4()), nome="Organizador A")
        org2 = Organizador(id=str(uuid.uuid4()), nome="Organizador B")
        org3 = Organizador(id=str(uuid.uuid4()), nome="Organizador C")

        db_session.add_all([org1, org2, org3])
        db_session.flush()

        response = request_auth(client, "GET", "/admin/organizadores/", auth_token)

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3
        ids_retornados = [org["id"] for org in data]
        assert org1.id in ids_retornados
        assert org2.id in ids_retornados
        assert org3.id in ids_retornados

        for org in data:
            assert "id" in org
            assert "nome" in org
            assert isinstance(org["id"], str)
            assert isinstance(org["nome"], str)

    def test_listar_organizadores_empty(self, client, db_session, auth_token):
        """
        Sad Path: Lista vazia quando não há organizadores
        Given: Não existem organizadores no banco
        When: Faço uma requisição GET para /admin/organizadores/
        Then: Recebo status 200 e uma lista vazia
        """
        db_session.query(Organizador).delete()
        db_session.flush()

        response = request_auth(client, "GET", "/admin/organizadores/", auth_token)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_listar_organizadores_with_fixture(
        self, client, organizador_fixture, auth_token
    ):
        """
        Happy Path: Lista organizadores usando fixture
        Given: Existe um organizador criado pela fixture
        When: Faço uma requisição GET para /admin/organizadores/
        Then: Recebo status 200 e o organizador está na lista
        """
        response = request_auth(client, "GET", "/admin/organizadores/", auth_token)

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

        organizador_encontrado = next(
            (org for org in data if org["id"] == organizador_fixture["id"]), None
        )
        assert organizador_encontrado is not None
        assert organizador_encontrado["nome"] == organizador_fixture["nome"]

    def test_listar_organizadores_response_model(self, client, db_session, auth_token):
        """
        Happy Path: Valida que o response model está correto
        Given: Existe um organizador no banco
        When: Faço uma requisição GET para /admin/organizadores/
        Then: A resposta segue o schema OrganizadorResponse
        """
        org = Organizador(id=str(uuid.uuid4()), nome="Teste Response Model")
        db_session.add(org)
        db_session.flush()

        response = request_auth(client, "GET", "/admin/organizadores/", auth_token)

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

        for organizador in data:
            assert set(organizador.keys()) == {"id", "nome"}
            assert isinstance(organizador["id"], str)
            assert isinstance(organizador["nome"], str)
            assert len(organizador["id"]) > 0
            assert len(organizador["nome"]) > 0

    def test_listar_organizadores_multiple_calls(self, client, db_session, auth_token):
        """
        Happy Path: Múltiplas chamadas retornam resultados consistentes
        Given: Existem organizadores no banco
        When: Faço múltiplas requisições GET para /admin/organizadores/
        Then: Todas retornam os mesmos dados
        """
        org1 = Organizador(id=str(uuid.uuid4()), nome="Organizador Consistente 1")
        org2 = Organizador(id=str(uuid.uuid4()), nome="Organizador Consistente 2")
        db_session.add_all([org1, org2])
        db_session.flush()

        response1 = request_auth(client, "GET", "/admin/organizadores/", auth_token)
        response2 = request_auth(client, "GET", "/admin/organizadores/", auth_token)
        response3 = request_auth(client, "GET", "/admin/organizadores/", auth_token)

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        data1 = response1.json()
        data2 = response2.json()
        data3 = response3.json()

        assert len(data1) == len(data2) == len(data3)
        assert data1 == data2 == data3

    def test_listar_organizadores_special_characters(
        self, client, db_session, auth_token
    ):
        """
        Happy Path: Organizadores com caracteres especiais no nome
        Given: Existem organizadores com caracteres especiais
        When: Faço uma requisição GET para /admin/organizadores/
        Then: Os nomes são retornados corretamente
        """
        org1 = Organizador(id=str(uuid.uuid4()), nome="Organização São José & Cia.")
        org2 = Organizador(id=str(uuid.uuid4()), nome="Associação Tênis Críquete")
        org3 = Organizador(id=str(uuid.uuid4()), nome="ONG Ação™")

        db_session.add_all([org1, org2, org3])
        db_session.flush()

        response = request_auth(client, "GET", "/admin/organizadores/", auth_token)

        assert response.status_code == 200

        data = response.json()
        nomes = [org["nome"] for org in data]

        assert "Organização São José & Cia." in nomes
        assert "Associação Tênis Críquete" in nomes
        assert "ONG Ação™" in nomes

    @pytest.mark.parametrize(
        "nome_organizador",
        [
            "A",
            "Org" * 100,
            "123 Números Primeiro",
            "   Espaços Antes",
        ],
    )
    def test_listar_organizadores_edge_cases(
        self, client, db_session, auth_token, nome_organizador
    ):
        """
        Happy Path: Lista organizadores com nomes edge case
        Given: Existem organizadores com nomes nos limites de validação
        When: Faço uma requisição GET para /admin/organizadores/
        Then: Todos são listados corretamente
        """
        org = Organizador(id=str(uuid.uuid4()), nome=nome_organizador)
        db_session.add(org)
        db_session.flush()

        response = request_auth(client, "GET", "/admin/organizadores/", auth_token)

        assert response.status_code == 200

        data = response.json()
        nomes = [o["nome"] for o in data]
        assert nome_organizador in nomes


class TestListarOrganizadoresErrorHandling:
    """Testes de tratamento de erros e casos extremos"""

    def test_listar_organizadores_invalid_method(self, client, auth_token):
        """
        Sad Path: Método HTTP inválido
        Given: Endpoint configurado apenas para GET
        When: Faço uma requisição POST para /admin/organizadores/
        Then: Recebo status 405 Method Not Allowed
        """
        response = request_auth(
            client, "POST", "/admin/organizadores/", auth_token, json={}
        )

        assert response.status_code == 422

    def test_listar_organizadores_invalid_path(self, client):
        """
        Sad Path: Caminho inválido
        Given: Endpoint é /organizadores/
        When: Faço uma requisição para /organizadores/invalid
        Then: Recebo status 404 Not Found
        """
        response = request(client, "GET", "/organizadores/invalid")

        assert response.status_code == 404

    def test_listar_organizadores_with_query_params(
        self, client, db_session, auth_token
    ):
        """
        Sad Path: Query parameters são ignorados (endpoint não os suporta)
        Given: Endpoint não aceita query parameters
        When: Faço requisição com query parameters
        Then: Parâmetros são ignorados e lista completa é retornada
        """
        org1 = Organizador(id=str(uuid.uuid4()), nome="Organizador Query 1")
        org2 = Organizador(id=str(uuid.uuid4()), nome="Organizador Query 2")
        db_session.add_all([org1, org2])
        db_session.flush()

        response = request_auth(
            client, "GET", "/admin/organizadores/?nome=Query&page=1", auth_token
        )

        assert response.status_code == 200

        data = response.json()
        assert len(data) >= 2

    def test_listar_organizadores_content_type(
        self, client, organizador_fixture, auth_token
    ):
        """
        Happy Path: Content-Type da resposta é JSON
        Given: Endpoint retorna JSON
        When: Faço uma requisição GET para /admin/organizadores/
        Then: Content-Type é application/json
        """
        response = request_auth(client, "GET", "/admin/organizadores/", auth_token)

        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]


class TestGetOrganizadorById:
    """Testes para o endpoint GET /organizadores/{id}"""

    def test_get_organizador_by_id_success(self, client, db_session, auth_token):
        """
        Happy Path: Busca organizador por ID com sucesso
        Given: Existe um organizador cadastrado no banco
        When: Faço uma requisição GET para /admin/organizadores/{id}
        Then: Recebo status 200 e os dados do organizador
        """
        org_id = str(uuid.uuid4())
        org = Organizador(id=org_id, nome="Organizador Teste")
        db_session.add(org)
        db_session.flush()

        response = request_auth(
            client, "GET", f"/admin/organizadores/{org_id}", auth_token
        )

        assert response.status_code == 200

        data = response.json()
        assert data["id"] == org_id
        assert data["nome"] == "Organizador Teste"
        assert set(data.keys()) == {"id", "nome"}

    def test_get_organizador_by_id_with_fixture(
        self, client, organizador_fixture, auth_token
    ):
        """
        Happy Path: Busca organizador usando fixture
        Given: Existe um organizador criado pela fixture
        When: Faço uma requisição GET para /admin/organizadores/{id}
        Then: Recebo status 200 e os dados do organizador
        """
        response = request_auth(
            client,
            "GET",
            f"/admin/organizadores/{organizador_fixture['id']}",
            auth_token,
        )

        assert response.status_code == 200

        data = response.json()
        assert data["id"] == organizador_fixture["id"]
        assert data["nome"] == organizador_fixture["nome"]

    def test_get_organizador_by_id_not_found(self, client, auth_token):
        """
        Sad Path: Organizador não encontrado
        Given: Não existe organizador com o ID fornecido
        When: Faço uma requisição GET para /admin/organizadores/{id}
        Then: Recebo status 404 e mensagem de erro
        """
        fake_id = str(uuid.uuid4())

        response = request_auth(
            client, "GET", f"/admin/organizadores/{fake_id}", auth_token
        )

        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "não encontrado" in data["detail"].lower()

    def test_get_organizador_by_id_invalid_uuid(self, client, auth_token):
        """
        Sad Path: ID no formato inválido
        Given: ID não é um UUID válido
        When: Faço uma requisição GET para /admin/organizadores/{id}
        Then: Recebo status 404 (não encontrado)
        """
        response = request_auth(
            client, "GET", "/admin/organizadores/invalid-id-123", auth_token
        )

        assert response.status_code == 404

    def test_get_organizador_by_id_special_characters(
        self, client, db_session, auth_token
    ):
        """
        Happy Path: Organizador com caracteres especiais no nome
        Given: Existe organizador com caracteres especiais
        When: Faço uma requisição GET para /admin/organizadores/{id}
        Then: Caracteres especiais são preservados
        """
        org_id = str(uuid.uuid4())
        org = Organizador(id=org_id, nome="Associação São José & Cia™")
        db_session.add(org)
        db_session.flush()

        response = request_auth(
            client, "GET", f"/admin/organizadores/{org_id}", auth_token
        )

        assert response.status_code == 200

        data = response.json()
        assert data["nome"] == "Associação São José & Cia™"

    def test_get_organizador_by_id_unicode(self, client, db_session, auth_token):
        """
        Happy Path: Organizador com Unicode
        Given: Existe organizador com caracteres Unicode
        When: Faço uma requisição GET para /admin/organizadores/{id}
        Then: Unicode é preservado
        """
        org_id = str(uuid.uuid4())
        org = Organizador(id=org_id, nome="组织 Chinese 🎉")
        db_session.add(org)
        db_session.flush()

        response = request_auth(
            client, "GET", f"/admin/organizadores/{org_id}", auth_token
        )

        assert response.status_code == 200

        data = response.json()
        assert data["nome"] == "组织 Chinese 🎉"

    def test_get_organizador_by_id_multiple_calls(self, client, db_session, auth_token):
        """
        Happy Path: Múltiplas chamadas retornam dados consistentes
        Given: Existe um organizador no banco
        When: Faço múltiplas requisições GET para /admin/organizadores/{id}
        Then: Todas retornam os mesmos dados
        """
        org_id = str(uuid.uuid4())
        org = Organizador(id=org_id, nome="Organizador Consistente")
        db_session.add(org)
        db_session.flush()

        response1 = request_auth(
            client, "GET", f"/admin/organizadores/{org_id}", auth_token
        )
        response2 = request_auth(
            client, "GET", f"/admin/organizadores/{org_id}", auth_token
        )
        response3 = request_auth(
            client, "GET", f"/admin/organizadores/{org_id}", auth_token
        )

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        data1 = response1.json()
        data2 = response2.json()
        data3 = response3.json()

        assert data1 == data2 == data3

    def test_get_organizador_by_id_response_schema(
        self, client, db_session, auth_token
    ):
        """
        Happy Path: Valida schema da resposta
        Given: Existe um organizador no banco
        When: Faço uma requisição GET para /admin/organizadores/{id}
        Then: Resposta segue o schema OrganizadorResponse
        """
        org_id = str(uuid.uuid4())
        org = Organizador(id=org_id, nome="Schema Test")
        db_session.add(org)
        db_session.flush()

        response = request_auth(
            client, "GET", f"/admin/organizadores/{org_id}", auth_token
        )

        assert response.status_code == 200

        data = response.json()
        assert set(data.keys()) == {"id", "nome"}
        assert isinstance(data["id"], str)
        assert isinstance(data["nome"], str)
        assert len(data["id"]) > 0
        assert len(data["nome"]) > 0

    def test_get_organizador_by_id_content_type(self, client, db_session, auth_token):
        """
        Happy Path: Content-Type da resposta é JSON
        Given: Existe um organizador no banco
        When: Faço uma requisição GET para /admin/organizadores/{id}
        Then: Content-Type é application/json
        """
        org_id = str(uuid.uuid4())
        org = Organizador(id=org_id, nome="Content Type Test")
        db_session.add(org)
        db_session.flush()

        response = request_auth(
            client, "GET", f"/admin/organizadores/{org_id}", auth_token
        )

        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]


class TestGetOrganizadorByIdErrorHandling:
    """Testes de tratamento de erros para GET by ID"""

    def test_get_organizador_by_id_empty_id(self, client, auth_token):
        """
        Sad Path: ID vazio redireciona para lista
        Given: ID vazio na URL
        When: Faço uma requisição GET para /admin/organizadores/
        Then: Retorna lista (endpoint diferente)
        """
        response = request_auth(client, "GET", "/admin/organizadores/", auth_token)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.parametrize(
        "invalid_id",
        [
            "00000000-0000-0000-0000-000000000000",
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "123e4567-e89b-12d3-a456-426614174000",
        ],
    )
    def test_get_organizador_by_id_valid_uuid_not_found(
        self, client, auth_token, invalid_id
    ):
        """
        Sad Path: UUID válido mas organizador não existe
        Given: ID é um UUID válido mas não existe no banco
        When: Faço uma requisição GET para /admin/organizadores/{id}
        Then: Recebo status 404
        """
        response = request_auth(
            client, "GET", f"/admin/organizadores/{invalid_id}", auth_token
        )

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
