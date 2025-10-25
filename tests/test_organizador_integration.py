
import uuid

import pytest

from app.models.organizador_model import Organizador
from tests.helpers import request


class TestListarOrganizadores:
    """Testes para o endpoint GET /organizadores/"""

    def test_listar_organizadores_success(self, client, db_session):
        """
        Happy Path: Lista organizadores com sucesso
        Given: Existem organizadores cadastrados no banco
        When: Faço uma requisição GET para /organizadores/
        Then: Recebo status 200 e a lista de organizadores
        """
        org1 = Organizador(id=str(uuid.uuid4()), nome="Organizador A")
        org2 = Organizador(id=str(uuid.uuid4()), nome="Organizador B")
        org3 = Organizador(id=str(uuid.uuid4()), nome="Organizador C")

        db_session.add_all([org1, org2, org3])
        db_session.flush()

        response = request(client, "GET", "/organizadores/")

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

    def test_listar_organizadores_empty(self, client, db_session):
        """
        Sad Path: Lista vazia quando não há organizadores
        Given: Não existem organizadores no banco
        When: Faço uma requisição GET para /organizadores/
        Then: Recebo status 200 e uma lista vazia
        """
        db_session.query(Organizador).delete()
        db_session.flush()

        response = request(client, "GET", "/organizadores/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_listar_organizadores_with_fixture(self, client, organizador_fixture):
        """
        Happy Path: Lista organizadores usando fixture
        Given: Existe um organizador criado pela fixture
        When: Faço uma requisição GET para /organizadores/
        Then: Recebo status 200 e o organizador está na lista
        """
        response = request(client, "GET", "/organizadores/")

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

        organizador_encontrado = next(
            (org for org in data if org["id"] == organizador_fixture["id"]), None
        )
        assert organizador_encontrado is not None
        assert organizador_encontrado["nome"] == organizador_fixture["nome"]

    def test_listar_organizadores_response_model(self, client, db_session):
        """
        Happy Path: Valida que o response model está correto
        Given: Existe um organizador no banco
        When: Faço uma requisição GET para /organizadores/
        Then: A resposta segue o schema OrganizadorResponse
        """
        org = Organizador(id=str(uuid.uuid4()), nome="Teste Response Model")
        db_session.add(org)
        db_session.flush()

        response = request(client, "GET", "/organizadores/")

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

        for organizador in data:
            assert set(organizador.keys()) == {"id", "nome"}
            assert isinstance(organizador["id"], str)
            assert isinstance(organizador["nome"], str)
            assert len(organizador["id"]) > 0
            assert len(organizador["nome"]) > 0

    def test_listar_organizadores_multiple_calls(self, client, db_session):
        """
        Happy Path: Múltiplas chamadas retornam resultados consistentes
        Given: Existem organizadores no banco
        When: Faço múltiplas requisições GET para /organizadores/
        Then: Todas retornam os mesmos dados
        """
        org1 = Organizador(id=str(uuid.uuid4()), nome="Organizador Consistente 1")
        org2 = Organizador(id=str(uuid.uuid4()), nome="Organizador Consistente 2")
        db_session.add_all([org1, org2])
        db_session.flush()

        response1 = request(client, "GET", "/organizadores/")
        response2 = request(client, "GET", "/organizadores/")
        response3 = request(client, "GET", "/organizadores/")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        data1 = response1.json()
        data2 = response2.json()
        data3 = response3.json()

        assert len(data1) == len(data2) == len(data3)
        assert data1 == data2 == data3

    def test_listar_organizadores_special_characters(self, client, db_session):
        """
        Happy Path: Organizadores com caracteres especiais no nome
        Given: Existem organizadores com caracteres especiais
        When: Faço uma requisição GET para /organizadores/
        Then: Os nomes são retornados corretamente
        """
        org1 = Organizador(id=str(uuid.uuid4()), nome="Organização São José & Cia.")
        org2 = Organizador(id=str(uuid.uuid4()), nome="Associação Tênis Críquete")
        org3 = Organizador(id=str(uuid.uuid4()), nome="ONG Ação™")

        db_session.add_all([org1, org2, org3])
        db_session.flush()

        response = request(client, "GET", "/organizadores/")

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
        self, client, db_session, nome_organizador
    ):
        """
        Happy Path: Lista organizadores com nomes edge case
        Given: Existem organizadores com nomes nos limites de validação
        When: Faço uma requisição GET para /organizadores/
        Then: Todos são listados corretamente
        """
        org = Organizador(id=str(uuid.uuid4()), nome=nome_organizador)
        db_session.add(org)
        db_session.flush()

        response = request(client, "GET", "/organizadores/")

        assert response.status_code == 200

        data = response.json()
        nomes = [o["nome"] for o in data]
        assert nome_organizador in nomes


class TestListarOrganizadoresErrorHandling:
    """Testes de tratamento de erros e casos extremos"""

    def test_listar_organizadores_invalid_method(self, client):
        """
        Sad Path: Método HTTP inválido
        Given: Endpoint configurado apenas para GET
        When: Faço uma requisição POST para /organizadores/
        Then: Recebo status 405 Method Not Allowed
        """
        response = request(client, "POST", "/organizadores/", json={})

        assert response.status_code == 405

    def test_listar_organizadores_invalid_path(self, client):
        """
        Sad Path: Caminho inválido
        Given: Endpoint é /organizadores/
        When: Faço uma requisição para /organizadores/invalid
        Then: Recebo status 404 Not Found
        """
        response = request(client, "GET", "/organizadores/invalid")

        assert response.status_code == 404

    def test_listar_organizadores_with_query_params(self, client, db_session):
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

        response = request(client, "GET", "/organizadores/?nome=Query&page=1")

        assert response.status_code == 200

        data = response.json()
        assert len(data) >= 2  

    def test_listar_organizadores_content_type(self, client, organizador_fixture):
        """
        Happy Path: Content-Type da resposta é JSON
        Given: Endpoint retorna JSON
        When: Faço uma requisição GET para /organizadores/
        Then: Content-Type é application/json
        """
        response = request(client, "GET", "/organizadores/")

        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]

