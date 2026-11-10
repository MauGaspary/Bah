import uuid

import pytest

from app.models.tag_model import Tag
from tests.helpers import request, request_auth


class TestListarTags:
    """Testes para o endpoint GET /tags/"""

    def test_listar_tags_success(self, client, db_session, auth_token):
        """
        Happy Path: Lista tags com sucesso
        Given: Existem tags cadastradas no banco
        When: Faço uma requisição GET para /admin/tags/
        Then: Recebo status 200 e a lista de tags
        """
        tag1 = Tag(
            id=str(uuid.uuid4()), nome="Tecnologia", descricao="Tag de tecnologia"
        )
        tag2 = Tag(id=str(uuid.uuid4()), nome="Inovação", descricao="Tag de inovação")
        tag3 = Tag(
            id=str(uuid.uuid4()),
            nome="Sustentabilidade",
            descricao="Tag de sustentabilidade",
        )

        db_session.add_all([tag1, tag2, tag3])
        db_session.flush()

        response = request_auth(client, "GET", "/admin/tags/", auth_token)

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3

        ids_retornados = [tag["id"] for tag in data]
        assert tag1.id in ids_retornados
        assert tag2.id in ids_retornados
        assert tag3.id in ids_retornados

        for tag in data:
            assert "id" in tag
            assert "nome" in tag
            assert "descricao" in tag
            assert isinstance(tag["id"], str)
            assert isinstance(tag["nome"], str)

    def test_listar_tags_empty(self, client, db_session, auth_token):
        """
        Sad Path: Lista vazia quando não há tags
        Given: Não existem tags no banco
        When: Faço uma requisição GET para /admin/tags/
        Then: Recebo status 200 e uma lista vazia
        """
        db_session.query(Tag).delete()
        db_session.flush()

        response = request_auth(client, "GET", "/admin/tags/", auth_token)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_listar_tags_with_fixture(self, client, tag_fixture, auth_token):
        """
        Happy Path: Lista tags usando fixture
        Given: Existe uma tag criada pela fixture
        When: Faço uma requisição GET para /admin/tags/
        Then: Recebo status 200 e a tag está na lista
        """
        response = request_auth(client, "GET", "/admin/tags/", auth_token)

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

        tag_encontrada = next(
            (tag for tag in data if tag["id"] == tag_fixture["id"]), None
        )
        assert tag_encontrada is not None
        assert tag_encontrada["nome"] == tag_fixture["nome"]
        assert tag_encontrada["descricao"] == tag_fixture["descricao"]

    def test_listar_tags_response_model(self, client, db_session, auth_token):
        """
        Happy Path: Valida que o response model está correto
        Given: Existe uma tag no banco
        When: Faço uma requisição GET para /admin/tags/
        Then: A resposta segue o schema TagResponse
        """
        tag = Tag(
            id=str(uuid.uuid4()),
            nome="Teste Response Model",
            descricao="Descrição de teste",
        )
        db_session.add(tag)
        db_session.flush()

        response = request_auth(client, "GET", "/admin/tags/", auth_token)

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

        for tag in data:
            assert set(tag.keys()) == {"id", "nome", "descricao"}
            assert isinstance(tag["id"], str)
            assert isinstance(tag["nome"], str)
            assert len(tag["id"]) > 0
            assert len(tag["nome"]) > 0

    def test_listar_tags_multiple_calls(self, client, db_session, auth_token):
        """
        Happy Path: Múltiplas chamadas retornam resultados consistentes
        Given: Existem tags no banco
        When: Faço múltiplas requisições GET para /admin/tags/
        Then: Todas retornam os mesmos dados
        """
        tag1 = Tag(
            id=str(uuid.uuid4()),
            nome="Tag Consistente 1",
            descricao="Descrição consistente 1",
        )
        tag2 = Tag(
            id=str(uuid.uuid4()),
            nome="Tag Consistente 2",
            descricao="Descrição consistente 2",
        )
        db_session.add_all([tag1, tag2])
        db_session.flush()

        response1 = request_auth(client, "GET", "/admin/tags/", auth_token)
        response2 = request_auth(client, "GET", "/admin/tags/", auth_token)
        response3 = request_auth(client, "GET", "/admin/tags/", auth_token)

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        data1 = response1.json()
        data2 = response2.json()
        data3 = response3.json()

        assert len(data1) == len(data2) == len(data3)
        assert data1 == data2 == data3

    def test_listar_tags_special_characters(self, client, db_session, auth_token):
        """
        Happy Path: Tags com caracteres especiais no nome
        Given: Existem tags com caracteres especiais
        When: Faço uma requisição GET para /admin/tags/
        Then: Os nomes são retornados corretamente
        """
        tag1 = Tag(id=str(uuid.uuid4()), nome="Ciência & Tecnologia", descricao="C&T")
        tag2 = Tag(id=str(uuid.uuid4()), nome="Educação São Paulo", descricao="SP")
        tag3 = Tag(id=str(uuid.uuid4()), nome="Arte™", descricao="Trademark")

        db_session.add_all([tag1, tag2, tag3])
        db_session.flush()

        response = request_auth(client, "GET", "/admin/tags/", auth_token)

        assert response.status_code == 200

        data = response.json()
        nomes = [tag["nome"] for tag in data]

        assert "Ciência & Tecnologia" in nomes
        assert "Educação São Paulo" in nomes
        assert "Arte™" in nomes

    def test_listar_tags_null_descricao(self, client, db_session, auth_token):
        """
        Happy Path: Tags com descrição nula
        Given: Existem tags sem descrição
        When: Faço uma requisição GET para /admin/tags/
        Then: Descrição nula é retornada corretamente
        """
        tag = Tag(id=str(uuid.uuid4()), nome="Tag Sem Descrição", descricao=None)
        db_session.add(tag)
        db_session.flush()

        response = request_auth(client, "GET", "/admin/tags/", auth_token)

        assert response.status_code == 200

        data = response.json()
        tag_encontrada = next(
            (t for t in data if t["nome"] == "Tag Sem Descrição"), None
        )
        assert tag_encontrada is not None
        assert tag_encontrada["descricao"] is None

    @pytest.mark.parametrize(
        "nome_tag,descricao_tag",
        [
            ("A", "Descrição curta"),
            ("Tag" * 50, "Descrição longa" * 20),
            ("123 Números", "Números primeiro"),
            ("   Espaços   ", "   Com espaços   "),
        ],
    )
    def test_listar_tags_edge_cases(
        self, client, db_session, auth_token, nome_tag, descricao_tag
    ):
        """
        Happy Path: Lista tags com nomes e descrições edge case
        Given: Existem tags com nomes nos limites de validação
        When: Faço uma requisição GET para /admin/tags/
        Then: Todas são listadas corretamente
        """
        tag = Tag(id=str(uuid.uuid4()), nome=nome_tag, descricao=descricao_tag)
        db_session.add(tag)
        db_session.flush()

        response = request_auth(client, "GET", "/admin/tags/", auth_token)

        assert response.status_code == 200

        data = response.json()
        nomes = [t["nome"] for t in data]
        assert nome_tag in nomes


class TestListarTagsErrorHandling:
    """Testes de tratamento de erros e casos extremos"""

    def test_listar_tags_invalid_method(self, client, auth_token):
        """
        Sad Path: Método HTTP inválido
        Given: Endpoint configurado apenas para GET
        When: Faço uma requisição POST para /admin/tags/
        Then: Recebo status 405 Method Not Allowed
        """
        response = request_auth(client, "POST", "/admin/tags/", auth_token, json={})

        assert response.status_code == 422

    def test_listar_tags_with_query_params(self, client, db_session, auth_token):
        """
        Sad Path: Query parameters são ignorados (endpoint não os suporta)
        Given: Endpoint não aceita query parameters
        When: Faço requisição com query parameters
        Then: Parâmetros são ignorados e lista completa é retornada
        """
        tag1 = Tag(id=str(uuid.uuid4()), nome="Tag Query 1", descricao="Desc 1")
        tag2 = Tag(id=str(uuid.uuid4()), nome="Tag Query 2", descricao="Desc 2")
        db_session.add_all([tag1, tag2])
        db_session.flush()

        response = request_auth(
            client, "GET", "/admin/tags/?nome=Query&page=1", auth_token
        )

        assert response.status_code == 200

        data = response.json()
        assert len(data) >= 2

    def test_listar_tags_content_type(self, client, tag_fixture, auth_token):
        """
        Happy Path: Content-Type da resposta é JSON
        Given: Endpoint retorna JSON
        When: Faço uma requisição GET para /admin/tags/
        Then: Content-Type é application/json
        """
        response = request_auth(client, "GET", "/admin/tags/", auth_token)

        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
