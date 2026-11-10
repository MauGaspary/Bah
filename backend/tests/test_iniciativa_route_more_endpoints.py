from datetime import date, time

from fastapi.testclient import TestClient

from app.main import app
from app.models.iniciativa_horario_model import HorarioTipo
from app.routes import iniciativa_route as mod


class FakeCtl:
    def __init__(self, *_): ...
    def create_iniciativa(self, iniciativa, criado_por):
        return {
            "id": "1",
            "titulo": iniciativa.titulo,
            "descricao": iniciativa.descricao,
            "organizador_id": iniciativa.organizador_id,
            "link": iniciativa.link,
            "local": iniciativa.local,
            "imagem_url": iniciativa.imagem_url,
            "destaque": False,
            "horarios": [
                {
                    "id": "h",
                    "data_evento": iniciativa.horarios[0].data_evento,
                    "hora_inicio": iniciativa.horarios[0].hora_inicio,
                    "hora_fim": iniciativa.horarios[0].hora_fim,
                    "tipo": iniciativa.horarios[0].tipo,
                    "criado_em": None,
                }
            ],
            "criado_em": None,
            "criado_por": "sistema",
            "editado_em": None,
            "editado_por": None,
            "organizador": None,
            "tags": [],
            "descricoes_extras": [],
        }

    def get_calendario_mensal(self, data):
        return {"mes": f"{data.year:04d}-{data.month:02d}", "dias": []}

    def get_iniciativa_by_id(self, _id):
        return {
            "id": _id,
            "titulo": "t",
            "descricao": "descrição válida e longa",
            "organizador_id": "org",
            "link": "https://example.com",
            "local": "Centro",
            "imagem_url": "https://example.com/img.png",
            "destaque": False,
            "horarios": [
                {
                    "id": "h",
                    "data_evento": date(2025, 1, 1),
                    "hora_inicio": time(10, 0),
                    "hora_fim": time(11, 0),
                    "tipo": HorarioTipo.PRESENCIAL,
                    "criado_em": None,
                }
            ],
            "criado_em": None,
            "criado_por": "sistema",
            "editado_em": None,
            "editado_por": None,
            "organizador": None,
            "tags": [],
            "descricoes_extras": [],
        }

    def search_iniciativas(self, q, page, size):
        return {
            "items": [],
            "total": 0,
            "filters": {
                "q": q,
                "page": page,
                "size": size,
                "order_by": "criado_em",
                "order_dir": "desc",
                "created_from": None,
                "created_to": None,
            },
        }


def test_outros_endpoints(monkeypatch):
    monkeypatch.setattr(mod, "IniciativaController", FakeCtl)
    c = TestClient(app)

    payload = {
        "titulo": "X",
        "descricao": "Descrição válida com mais de 10 caracteres.",
        "organizador_id": "org",
        "link": "https://example.com",
        "local": "Centro",
        "imagem_url": "https://example.com/img.png",
        "destaque": False,
        "horarios": [
            {
                "data_evento": "2025-01-01",
                "hora_inicio": "10:00:00",
                "hora_fim": "11:00:00",
                "tipo": "presencial",
            }
        ],
        "tag_ids": [],
    }

    r = c.post("/iniciativas", json=payload, headers={"Authorization": "Bearer test"})
    assert r.status_code == 201, r.text

    r = c.get("/iniciativas/calendario", params={"data": "2025-01-01"})
    assert r.status_code == 200 and r.json()["mes"] == "2025-01"

    r = c.get("/iniciativas/abc", headers={"Authorization": "Bearer test"})
    assert r.status_code == 200 and r.json()["id"] == "abc"


def test_search_success(monkeypatch):
    monkeypatch.setattr(mod, "IniciativaController", FakeCtl)
    c = TestClient(app)
    r = c.get("/iniciativas/search", params={"q": "abc", "page": 1, "size": 10})
    assert r.status_code == 200
    body = r.json()
    assert body["filters"]["q"] == "abc"
    assert body["filters"]["page"] == 1
    assert body["filters"]["size"] == 10
