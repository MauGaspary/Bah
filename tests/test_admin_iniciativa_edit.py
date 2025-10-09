from datetime import datetime, timezone

import pytest

from tests.helpers import request_auth


def test_edit_iniciativa_success(client, iniciativa_fixture, auth_token):
    payload = {
        "titulo": "Título Atualizado",
        "descricao": "Descrição atualizada",
        "destaque": True,
    }

    response = request_auth(
        client,
        "PATCH",
        f"/admin/iniciativas/{iniciativa_fixture['id']}",
        token=auth_token,
        json=payload,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == payload["titulo"]
    assert data["descricao"] == payload["descricao"]
    assert data["destaque"] == payload["destaque"]
    assert data["id"] == iniciativa_fixture["id"]
    assert data["editado_em"] is not None
    assert data["editado_por"] is not None


def test_edit_iniciativa_partial_update(client, iniciativa_fixture, auth_token):
    """Teste: edição parcial mantém campos não enviados"""
    original_titulo = iniciativa_fixture["titulo"]
    payload = {"descricao": "Nova descrição apenas"}

    response = request_auth(
        client,
        "PATCH",
        f"/admin/iniciativas/{iniciativa_fixture['id']}",
        token=auth_token,
        json=payload,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == original_titulo  # Mantém título original
    assert data["descricao"] == payload["descricao"]


def test_edit_iniciativa_not_found(client, auth_token):
    """Teste: edição de iniciativa inexistente → 404"""
    payload = {"titulo": "Novo título"}

    response = request_auth(
        client,
        "PATCH",
        "/admin/iniciativas/id-inexistente",
        token=auth_token,
        json=payload,
    )

    assert response.status_code == 404
    data = response.json()
    assert "Iniciativa não encontrada" in data["detail"]


def test_edit_iniciativa_soft_deleted(
    client, iniciativa_fixture, auth_token, db_session
):
    from app.models.iniciativa_model import Iniciativa

    iniciativa = (
        db_session.query(Iniciativa)
        .filter(Iniciativa.id == iniciativa_fixture["id"])
        .first()
    )
    iniciativa.deletado_em = datetime.now(timezone.utc)
    db_session.commit()

    payload = {"titulo": "Novo título"}

    response = request_auth(
        client,
        "PATCH",
        f"/admin/iniciativas/{iniciativa_fixture['id']}",
        token=auth_token,
        json=payload,
    )

    assert response.status_code == 404
    data = response.json()
    assert "Iniciativa não encontrada" in data["detail"]


def test_edit_iniciativa_empty_payload(client, iniciativa_fixture, auth_token):
    """Teste: edição com payload vazio não altera nada"""
    payload = {}

    response = request_auth(
        client,
        "PATCH",
        f"/admin/iniciativas/{iniciativa_fixture['id']}",
        token=auth_token,
        json=payload,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == iniciativa_fixture["titulo"]
    assert data["organizador_id"] == iniciativa_fixture["organizador_id"]


def test_edit_iniciativa_all_fields(
    client, iniciativa_fixture, organizador_fixture, auth_token
):
    """Teste: edição de todos os campos permitidos"""
    payload = {
        "titulo": "Título Completamente Novo",
        "descricao": "Descrição completamente nova",
        "organizador_id": organizador_fixture["id"],
        "link": "https://novo-link.com",
        "local": "Novo Local",
        "imagem_url": "https://nova-imagem.com/img.jpg",
        "destaque": True,
    }

    response = request_auth(
        client,
        "PATCH",
        f"/admin/iniciativas/{iniciativa_fixture['id']}",
        token=auth_token,
        json=payload,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == payload["titulo"]
    assert data["descricao"] == payload["descricao"]
    assert data["organizador_id"] == payload["organizador_id"]
    assert data["link"] == payload["link"]
    assert data["local"] == payload["local"]
    assert data["imagem_url"] == payload["imagem_url"]
    assert data["destaque"] == payload["destaque"]
