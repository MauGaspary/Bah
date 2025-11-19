from datetime import date, time
from types import SimpleNamespace

import pytest

import app.services.iniciativa_service as mod
from app.models.iniciativa_horario_model import HorarioTipo
from app.schemas.iniciativa_schema import IniciativaCreate, IniciativaHorarioCreate
from app.services.iniciativa_service import IniciativaService


def _payload():
    return IniciativaCreate(
        titulo="t",
        descricao="d",
        organizador_id="org",
        link="https://l",
        local=None,
        imagem_url="https://img",
        destaque=False,
        horarios=[
            IniciativaHorarioCreate(
                data_evento=date(2025, 1, 1),
                hora_inicio=time(10),
                hora_fim=time(11),
                tipo=HorarioTipo.PRESENCIAL,
            )
        ],
        tag_ids=["t1", "t2"],
        descricoes_extras=["e1", "e2"],
    )


class RepoBase:
    def __init__(self):
        self.db = SimpleNamespace(
            query=lambda *_: SimpleNamespace(
                filter=lambda *_: SimpleNamespace(first=lambda: None)
            )
        )

    def organizador_exists(self, *_):
        return True

    def tags_exist(self, ids):
        return ids

    def check_duplicate_iniciativa(self, *_):
        return None

    def check_conflicting_horarios(self, *_):
        return []

    def create(self, *a, **k):
        return {
            "id": "1",
            "titulo": "t",
            "descricao": "d",
            "organizador_id": "org",
            "link": "https://l",
            "local": None,
            "imagem_url": "https://img",
            "destaque": False,
            "horarios": [
                {
                    "id": "h",
                    "data_evento": date(2025, 1, 1),
                    "hora_inicio": time(10),
                    "hora_fim": time(11),
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


def test_create_erro_usuario_inexistente_quando_criado_por_nao_sistema():
    svc = IniciativaService(db=None, model=object())
    r = RepoBase()
    r.db.query = lambda *_: SimpleNamespace(
        filter=lambda *_: SimpleNamespace(first=lambda: None)
    )
    svc.repository = r
    with pytest.raises(ValueError):
        svc.create_iniciativa(_payload(), criado_por="alguem")


def test_create_erro_sem_modelo_cobre_except():
    svc = IniciativaService(db=None, model=None)
    svc.repository = RepoBase()
    with pytest.raises(RuntimeError):
        svc.create_iniciativa(_payload(), criado_por="sistema")


def test_create_erro_organizador_inexistente():
    svc = IniciativaService(db=None, model=object())
    r = RepoBase()
    r.organizador_exists = lambda *_: False
    svc.repository = r
    with pytest.raises(ValueError):
        svc.create_iniciativa(_payload(), criado_por="sistema")


def test_create_erro_tags_inexistentes():
    svc = IniciativaService(db=None, model=object())
    r = RepoBase()
    r.tags_exist = lambda ids: ["t1"]
    svc.repository = r
    with pytest.raises(ValueError):
        svc.create_iniciativa(_payload(), criado_por="sistema")


def test_create_erro_duplicado():
    svc = IniciativaService(db=None, model=object())
    r = RepoBase()
    r.check_duplicate_iniciativa = lambda *_: object()
    svc.repository = r
    with pytest.raises(ValueError):
        svc.create_iniciativa(_payload(), criado_por="sistema")


def test_create_conflito_horarios_ramo_passado():
    svc = IniciativaService(
        db=None, model=SimpleNamespace(encode=lambda *a, **k: [0.0] * 768)
    )
    r = RepoBase()
    r.check_conflicting_horarios = lambda *_: [object()]
    svc.repository = r
    out = svc.create_iniciativa(_payload(), criado_por="sistema")
    assert out.titulo == "t"
