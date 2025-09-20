from datetime import date, time

import pytest

from tests.helpers import request, request_auth


def test_create_iniciativa_success(
    client, organizador_fixture, tag_fixture, usuario_fixture, auth_token
):
    """Teste de criação feliz: criação com payload mínimo válido → 201"""
    payload = {
        "titulo": "Iniciativa Teste",
        "descricao": "Descrição da iniciativa teste",
        "organizador_id": organizador_fixture["id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "horarios": [
            {
                "data_evento": "2025-12-01",
                "hora_inicio": "09:00:00",
                "hora_fim": "17:00:00",
                "tipo": "presencial",
            }
        ],
    }

    response = request_auth(
        client,
        "POST",
        f"/admin/iniciativas/?criado_por={usuario_fixture['id']}",
        token=auth_token,
        json=payload,
    )

    if response.status_code != 201:
        print(f"Erro: {response.status_code} - {response.json()}")

    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == payload["titulo"]
    assert data["descricao"] == payload["descricao"]
    assert data["organizador_id"] == payload["organizador_id"]
    assert data["link"] == payload["link"]
    assert data["imagem_url"] == payload["imagem_url"]
    assert data["destaque"] == False
    assert len(data["horarios"]) == 1
    assert data["horarios"][0]["data_evento"] == "2025-12-01"
    assert "id" in data


def test_create_iniciativa_with_tags(
    client, organizador_fixture, tag_fixture, usuario_fixture, auth_token
):
    """Teste de criação com tags"""
    payload = {
        "titulo": "Iniciativa com Tags",
        "descricao": "Descrição da iniciativa com tags",
        "organizador_id": organizador_fixture["id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "destaque": True,
        "local": "Porto Alegre",
        "tag_ids": [tag_fixture["id"]],
        "horarios": [
            {
                "data_evento": "2025-12-01",
                "hora_inicio": "09:00:00",
                "hora_fim": "17:00:00",
                "tipo": "online",
            }
        ],
    }

    response = request_auth(
        client,
        "POST",
        f"/admin/iniciativas/?criado_por={usuario_fixture['id']}",
        token=auth_token,
        json=payload,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == payload["titulo"]
    assert data["destaque"] == True
    assert data["local"] == payload["local"]


def test_create_iniciativa_multiple_horarios(
    client, organizador_fixture, usuario_fixture, auth_token
):
    """Teste de criação com múltiplos horários"""
    payload = {
        "titulo": "Iniciativa Múltiplos Horários",
        "descricao": "Descrição da iniciativa",
        "organizador_id": organizador_fixture["id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "horarios": [
            {
                "data_evento": "2025-12-01",
                "hora_inicio": "09:00:00",
                "hora_fim": "12:00:00",
                "tipo": "presencial",
            },
            {
                "data_evento": "2025-12-02",
                "hora_inicio": "14:00:00",
                "hora_fim": "18:00:00",
                "tipo": "hibrido",
            },
        ],
    }

    response = request_auth(
        client,
        "POST",
        f"/admin/iniciativas/?criado_por={usuario_fixture['id']}",
        token=auth_token,
        json=payload,
    )

    assert response.status_code == 201
    data = response.json()
    assert len(data["horarios"]) == 2


def test_create_iniciativa_missing_required_fields(client, auth_token):
    """Teste de falha: campos obrigatórios ausentes → 422"""
    payload = {"titulo": "Iniciativa Incompleta"}

    response = request_auth(
        client, "POST", "/admin/iniciativas/", token=auth_token, json=payload
    )

    assert response.status_code == 422


def test_create_iniciativa_empty_title(client, organizador_fixture, auth_token):
    """Teste de falha: título vazio → 422"""
    payload = {
        "titulo": "",
        "descricao": "Descrição válida",
        "organizador_id": organizador_fixture["id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "horarios": [
            {
                "data_evento": "2025-12-01",
                "hora_inicio": "09:00:00",
                "hora_fim": "17:00:00",
                "tipo": "presencial",
            }
        ],
    }

    response = request_auth(
        client, "POST", "/admin/iniciativas/", token=auth_token, json=payload
    )

    assert response.status_code == 422


def test_create_iniciativa_empty_horarios(client, organizador_fixture, auth_token):
    """Teste de falha: lista de horários vazia → 422"""
    payload = {
        "titulo": "Iniciativa Sem Horários",
        "descricao": "Descrição válida",
        "organizador_id": organizador_fixture["id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "horarios": [],
    }

    response = request_auth(
        client, "POST", "/admin/iniciativas/", token=auth_token, json=payload
    )

    assert response.status_code == 422


def test_create_iniciativa_hora_fim_menor_que_inicio(
    client, organizador_fixture, auth_token
):
    """Teste de falha: hora_fim < hora_inicio → 422"""
    payload = {
        "titulo": "Iniciativa Horário Inválido",
        "descricao": "Descrição válida",
        "organizador_id": organizador_fixture["id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "horarios": [
            {
                "data_evento": "2025-12-01",
                "hora_inicio": "17:00:00",
                "hora_fim": "09:00:00",
                "tipo": "presencial",
            }
        ],
    }

    response = request_auth(
        client, "POST", "/admin/iniciativas/", token=auth_token, json=payload
    )

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    if isinstance(data["detail"], list):
        error_messages = [error.get("msg", "") for error in data["detail"]]
        assert any(
            "Hora de fim deve ser maior que hora de início" in msg
            for msg in error_messages
        )
    else:
        assert "Hora de fim deve ser maior que hora de início" in data["detail"]


def test_create_iniciativa_organizador_inexistente(client, auth_token):
    """Teste de falha: organizador inexistente → 422"""
    payload = {
        "titulo": "Iniciativa Organizador Inválido",
        "descricao": "Descrição válida",
        "organizador_id": "organizador-inexistente",
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "horarios": [
            {
                "data_evento": "2025-12-01",
                "hora_inicio": "09:00:00",
                "hora_fim": "17:00:00",
                "tipo": "presencial",
            }
        ],
    }

    response = request_auth(
        client, "POST", "/admin/iniciativas/", token=auth_token, json=payload
    )

    assert response.status_code == 422
    data = response.json()
    assert "Organizador não encontrado" in data["detail"]


def test_create_iniciativa_tag_inexistente(client, organizador_fixture, auth_token):
    """Teste de falha: tag inexistente → 422"""
    payload = {
        "titulo": "Iniciativa Tag Inválida",
        "descricao": "Descrição válida",
        "organizador_id": organizador_fixture["id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "tag_ids": ["tag-inexistente"],
        "horarios": [
            {
                "data_evento": "2025-12-01",
                "hora_inicio": "09:00:00",
                "hora_fim": "17:00:00",
                "tipo": "presencial",
            }
        ],
    }

    response = request_auth(
        client, "POST", "/admin/iniciativas/", token=auth_token, json=payload
    )

    assert response.status_code == 422
    data = response.json()
    assert "Tags não encontradas" in data["detail"]


def test_create_iniciativa_duplicada(
    client, organizador_fixture, iniciativa_fixture, auth_token
):
    """Teste de alerta: possível duplicado (mesmo título e organizador)"""
    payload = {
        "titulo": iniciativa_fixture["titulo"],
        "descricao": "Descrição diferente",
        "organizador_id": iniciativa_fixture["organizador_id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "horarios": [
            {
                "data_evento": "2025-12-01",
                "hora_inicio": "09:00:00",
                "hora_fim": "17:00:00",
                "tipo": "presencial",
            }
        ],
    }

    response = request_auth(
        client, "POST", "/admin/iniciativas/", token=auth_token, json=payload
    )

    assert response.status_code == 422
    data = response.json()
    assert (
        "Já existe uma iniciativa com este título para este organizador"
        in data["detail"]
    )


def test_get_iniciativa_by_id_success(client, iniciativa_fixture, auth_token):
    """Teste de busca por ID com sucesso"""
    response = request_auth(
        client,
        "GET",
        f"/admin/iniciativas/{iniciativa_fixture['id']}",
        token=auth_token,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == iniciativa_fixture["id"]
    assert data["titulo"] == iniciativa_fixture["titulo"]


def test_get_iniciativa_by_id_not_found(client, auth_token):
    """Teste de busca por ID inexistente"""
    response = request_auth(
        client, "GET", "/admin/iniciativas/id-inexistente", token=auth_token
    )

    assert response.status_code == 404
    data = response.json()
    assert "Iniciativa não encontrada" in data["detail"]


def test_delete_iniciativa_success(client, iniciativa_fixture, auth_token, db_session):
    """Teste feliz: DELETE → 204 → iniciativa não aparece mais na listagem"""

    # Verifica se a iniciativa existe na listagem
    response_list_before = request_auth(
        client, "GET", "/admin/iniciativas", token=auth_token
    )
    assert response_list_before.status_code == 200
    iniciativa_ids_before = [item["id"] for item in response_list_before.json()["items"]]
    assert iniciativa_fixture["id"] in iniciativa_ids_before

    # DELETE
    response_delete = request_auth(
        client,
        "DELETE",
        f"/admin/iniciativas/{iniciativa_fixture['id']}",
        token=auth_token
    )
    assert response_delete.status_code == 204

    # Verifica se não aparece mais na listagem
    response_list_after = request_auth(
        client, "GET", "/admin/iniciativas", token=auth_token
    )
    assert response_list_after.status_code == 200
    iniciativas_ids_after = [item["id"] for item in response_list_after.json()["items"]]
    assert iniciativa_fixture["id"] not in iniciativas_ids_after

    # Verifica se deletado_em foi atualizado no banco de dados
    from app.models.iniciativa_model import Iniciativa
    deleted_iniciativa = db_session.query(Iniciativa).filter(
        Iniciativa.id == iniciativa_fixture["id"]
    ).first()
    assert deleted_iniciativa.deletado_em is not None
    assert deleted_iniciativa.deletado_por is not None


def test_delete_iniciativa_idempotente(client, iniciativa_fixture, auth_token):
    """Teste de idempotência: DELETE duas vezes → 204 nas duas"""

    # Primeiro DELETE
    response1 = request_auth(
        client, 
        "DELETE",
        f"/admin/iniciativas/{iniciativa_fixture['id']}",  
        token=auth_token
    )
    assert response1.status_code == 204

    # Segundo DELETE
    response2 = request_auth(
        client, 
        "DELETE",
        f"/admin/iniciativas/{iniciativa_fixture['id']}",  
        token=auth_token
    )
    assert response2.status_code == 204


def test_delete_iniciativa_inexistente(client, auth_token):
    """Teste de iniciativa inexistente → 404"""
    response = request_auth(
        client,
        "DELETE",
        "/admin/iniciativas/99999999-9999-9999-9999-999999999999",  
        token=auth_token
    )
    assert response.status_code == 404
    assert "não encontrada" in response.json()["detail"].lower()


def test_delete_iniciativa_nao_autorizada(client, iniciativa_fixture):
    """Teste de DELETE sem autenticação → 401"""
    response = request(
        client,
        "DELETE",
        f"/admin/iniciativas/{iniciativa_fixture['id']}"
    )
    assert response.status_code == 401