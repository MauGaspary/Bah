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


def test_calendario_mes_sem_eventos(client):
    """Teste: mês sem eventos → todos os dias com lista vazia"""
    response = request(client, "GET", "/iniciativas/calendario?data=2030-01-15")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["mes"] == "2030-01"
    
    assert len(data["dias"]) == 31
    
    for dia in data["dias"]:
        assert "data" in dia
        assert "iniciativas" in dia
        assert dia["iniciativas"] == []
    
   
    datas = [dia["data"] for dia in data["dias"]]
    assert datas == sorted(datas)
    
    assert data["dias"][0]["data"] == "2030-01-01"
    assert data["dias"][-1]["data"] == "2030-01-31"


def test_calendario_fevereiro_ano_bissexto(client):
    """Teste: fevereiro de ano bissexto tem 29 dias"""
    response = request(client, "GET", "/iniciativas/calendario?data=2024-02-15")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["mes"] == "2024-02"
    
    assert len(data["dias"]) == 29
    
    assert data["dias"][0]["data"] == "2024-02-01"
    assert data["dias"][-1]["data"] == "2024-02-29"


def test_calendario_fevereiro_ano_comum(client):
    """Teste: fevereiro de ano comum tem 28 dias"""
    response = request(client, "GET", "/iniciativas/calendario?data=2025-02-15")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["mes"] == "2025-02"
    
    assert len(data["dias"]) == 28
    
    assert data["dias"][0]["data"] == "2025-02-01"
    assert data["dias"][-1]["data"] == "2025-02-28"


def test_calendario_bordas_primeiro_ultimo_dia(
    client, organizador_fixture, usuario_fixture, auth_token
):
    """Teste: iniciativas no primeiro e último dia do mês aparecem corretamente"""
    payload_primeiro_dia = {
        "titulo": "Iniciativa Primeiro Dia",
        "descricao": "Evento no primeiro dia do mês",
        "organizador_id": organizador_fixture["id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "horarios": [
            {
                "data_evento": "2025-10-01", 
                "hora_inicio": "09:00:00",
                "hora_fim": "12:00:00",
                "tipo": "presencial",
            }
        ],
    }
    
    response1 = request_auth(
        client,
        "POST",
        f"/admin/iniciativas/?criado_por={usuario_fixture['id']}",
        token=auth_token,
        json=payload_primeiro_dia,
    )
    assert response1.status_code == 201
    
    payload_ultimo_dia = {
        "titulo": "Iniciativa Último Dia",
        "descricao": "Evento no último dia do mês",
        "organizador_id": organizador_fixture["id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "horarios": [
            {
                "data_evento": "2025-10-31", 
                "hora_inicio": "14:00:00",
                "hora_fim": "18:00:00",
                "tipo": "online",
            }
        ],
    }
    
    response2 = request_auth(
        client,
        "POST",
        f"/admin/iniciativas/?criado_por={usuario_fixture['id']}",
        token=auth_token,
        json=payload_ultimo_dia,
    )
    assert response2.status_code == 201
    
    response = request(client, "GET", "/iniciativas/calendario?data=2025-10-15")
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["dias"]) == 31
    
    primeiro_dia = data["dias"][0]
    assert primeiro_dia["data"] == "2025-10-01"
    assert len(primeiro_dia["iniciativas"]) == 1
    assert primeiro_dia["iniciativas"][0]["titulo"] == "Iniciativa Primeiro Dia"
    assert primeiro_dia["iniciativas"][0]["hora_inicio"] == "09:00:00"
    
    ultimo_dia = data["dias"][30]
    assert ultimo_dia["data"] == "2025-10-31"
    assert len(ultimo_dia["iniciativas"]) == 1
    assert ultimo_dia["iniciativas"][0]["titulo"] == "Iniciativa Último Dia"
    assert ultimo_dia["iniciativas"][0]["hora_inicio"] == "14:00:00"


def test_calendario_soft_delete_nao_aparece(
    client, organizador_fixture, usuario_fixture, auth_token
):
    """Teste: iniciativas soft-deletadas não aparecem no calendário"""
    payload = {
        "titulo": "Iniciativa Para Deletar",
        "descricao": "Será deletada (soft delete)",
        "organizador_id": organizador_fixture["id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "horarios": [
            {
                "data_evento": "2025-11-15",
                "hora_inicio": "10:00:00",
                "hora_fim": "12:00:00",
                "tipo": "presencial",
            }
        ],
    }
    
    response_create = request_auth(
        client,
        "POST",
        f"/admin/iniciativas/?criado_por={usuario_fixture['id']}",
        token=auth_token,
        json=payload,
    )
    assert response_create.status_code == 201
    iniciativa_id = response_create.json()["id"]
    
    response_antes = request(client, "GET", "/iniciativas/calendario?data=2025-11-15")
    assert response_antes.status_code == 200
    data_antes = response_antes.json()
    
    
    dia_15_antes = [dia for dia in data_antes["dias"] if dia["data"] == "2025-11-15"][0]
    assert len(dia_15_antes["iniciativas"]) >= 1
    assert any(
        ini["titulo"] == "Iniciativa Para Deletar" 
        for ini in dia_15_antes["iniciativas"]
    )
    
    from datetime import datetime
    from app.models.iniciativa_model import Iniciativa
    from app.config.database import SessionLocal
    
    db = SessionLocal()
    try:
        iniciativa = db.query(Iniciativa).filter(Iniciativa.id == iniciativa_id).first()
        iniciativa.deletado_em = datetime.utcnow()
        iniciativa.deletado_por = usuario_fixture['id']
        db.commit()
    finally:
        db.close()
    
    response_depois = request(client, "GET", "/iniciativas/calendario?data=2025-11-15")
    assert response_depois.status_code == 200
    data_depois = response_depois.json()

    dia_15_depois = [dia for dia in data_depois["dias"] if dia["data"] == "2025-11-15"][0]
    
    assert not any(
        ini["titulo"] == "Iniciativa Para Deletar" 
        for ini in dia_15_depois["iniciativas"]
    )


def test_calendario_multiplos_horarios_mesmo_dia_ordenacao(
    client, organizador_fixture, usuario_fixture, auth_token
):
    """Teste: dois horários no mesmo dia → 09:00 antes de 14:00; empate por título"""
    payload1 = {
        "titulo": "B - Iniciativa Tarde",
        "descricao": "Evento da tarde",
        "organizador_id": organizador_fixture["id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "horarios": [
            {
                "data_evento": "2025-12-10",
                "hora_inicio": "14:00:00",
                "hora_fim": "18:00:00",
                "tipo": "online",
            }
        ],
    }
    
    response1 = request_auth(
        client,
        "POST",
        f"/admin/iniciativas/?criado_por={usuario_fixture['id']}",
        token=auth_token,
        json=payload1,
    )
    assert response1.status_code == 201
    
    payload2 = {
        "titulo": "A - Iniciativa Manhã",
        "descricao": "Evento da manhã",
        "organizador_id": organizador_fixture["id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "horarios": [
            {
                "data_evento": "2025-12-10",
                "hora_inicio": "09:00:00",
                "hora_fim": "12:00:00",
                "tipo": "presencial",
            }
        ],
    }
    
    response2 = request_auth(
        client,
        "POST",
        f"/admin/iniciativas/?criado_por={usuario_fixture['id']}",
        token=auth_token,
        json=payload2,
    )
    assert response2.status_code == 201
    
    payload3 = {
        "titulo": "Z - Iniciativa Último Nome",
        "descricao": "Evento com nome Z",
        "organizador_id": organizador_fixture["id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "horarios": [
            {
                "data_evento": "2025-12-10",
                "hora_inicio": "09:00:00",
                "hora_fim": "11:00:00",
                "tipo": "hibrido",
            }
        ],
    }
    
    response3 = request_auth(
        client,
        "POST",
        f"/admin/iniciativas/?criado_por={usuario_fixture['id']}",
        token=auth_token,
        json=payload3,
    )
    assert response3.status_code == 201
    
    response = request(client, "GET", "/iniciativas/calendario?data=2025-12-10")
    
    assert response.status_code == 200
    data = response.json()
    
    dia_10 = [dia for dia in data["dias"] if dia["data"] == "2025-12-10"][0]
    
    assert len(dia_10["iniciativas"]) == 3
    
    iniciativas = dia_10["iniciativas"]
    
    assert iniciativas[0]["hora_inicio"] == "09:00:00"
    assert iniciativas[0]["titulo"] == "A - Iniciativa Manhã"
    
    assert iniciativas[1]["hora_inicio"] == "09:00:00"
    assert iniciativas[1]["titulo"] == "Z - Iniciativa Último Nome"
    
    
    assert iniciativas[2]["hora_inicio"] == "14:00:00"
    assert iniciativas[2]["titulo"] == "B - Iniciativa Tarde"


def test_calendario_com_tags(
    client, organizador_fixture, tag_fixture, usuario_fixture, auth_token
):
    """Teste: calendário retorna tags das iniciativas"""
    payload = {
        "titulo": "Iniciativa Com Tags",
        "descricao": "Evento com tags",
        "organizador_id": organizador_fixture["id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "tag_ids": [tag_fixture["id"]],
        "horarios": [
            {
                "data_evento": "2025-12-20",
                "hora_inicio": "10:00:00",
                "hora_fim": "12:00:00",
                "tipo": "presencial",
            }
        ],
    }
    
    response_create = request_auth(
        client,
        "POST",
        f"/admin/iniciativas/?criado_por={usuario_fixture['id']}",
        token=auth_token,
        json=payload,
    )
    assert response_create.status_code == 201
    
    response = request(client, "GET", "/iniciativas/calendario?data=2025-12-20")
    
    assert response.status_code == 200
    data = response.json()
    
    dia_20 = [dia for dia in data["dias"] if dia["data"] == "2025-12-20"][0]
    
    assert len(dia_20["iniciativas"]) >= 1
    
    iniciativa = next(
        ini for ini in dia_20["iniciativas"] 
        if ini["titulo"] == "Iniciativa Com Tags"
    )
    
    assert "tags" in iniciativa
    assert len(iniciativa["tags"]) == 1
    assert iniciativa["tags"][0]["id"] == tag_fixture["id"]
    assert iniciativa["tags"][0]["nome"] == tag_fixture["nome"]


def test_calendario_todos_campos_presentes(
    client, organizador_fixture, usuario_fixture, auth_token
):
    """Teste: verifica que todos os campos do schema estão presentes"""
    payload = {
        "titulo": "Iniciativa Completa",
        "descricao": "Evento com todos os campos",
        "organizador_id": organizador_fixture["id"],
        "link": "https://example.com",
        "imagem_url": "https://example.com/image.jpg",
        "local": "Porto Alegre",
        "destaque": True,
        "horarios": [
            {
                "data_evento": "2026-01-15",
                "hora_inicio": "10:00:00",
                "hora_fim": "12:00:00",
                "tipo": "hibrido",
            }
        ],
    }
    
    response_create = request_auth(
        client,
        "POST",
        f"/admin/iniciativas/?criado_por={usuario_fixture['id']}",
        token=auth_token,
        json=payload,
    )
    assert response_create.status_code == 201
    
    response = request(client, "GET", "/iniciativas/calendario?data=2026-01-15")
    
    assert response.status_code == 200
    data = response.json()
    
    dia_15 = [dia for dia in data["dias"] if dia["data"] == "2026-01-15"][0]
    
    assert len(dia_15["iniciativas"]) >= 1
    
    iniciativa = next(
        ini for ini in dia_15["iniciativas"] 
        if ini["titulo"] == "Iniciativa Completa"
    )
    
    assert "iniciativa_id" in iniciativa
    assert "horario_id" in iniciativa
    assert "titulo" in iniciativa
    assert iniciativa["titulo"] == "Iniciativa Completa"
    assert "descricao" in iniciativa
    assert iniciativa["descricao"] == "Evento com todos os campos"
    assert "hora_inicio" in iniciativa
    assert iniciativa["hora_inicio"] == "10:00:00"
    assert "hora_fim" in iniciativa
    assert iniciativa["hora_fim"] == "12:00:00"
    assert "tipo" in iniciativa
    assert iniciativa["tipo"] == "hibrido"
    assert "link" in iniciativa
    assert iniciativa["link"] == "https://example.com"
    assert "local" in iniciativa
    assert iniciativa["local"] == "Porto Alegre"
    assert "imagem_url" in iniciativa
    assert iniciativa["imagem_url"] == "https://example.com/image.jpg"
    assert "destaque" in iniciativa
    assert iniciativa["destaque"] == True
    assert "tags" in iniciativa
