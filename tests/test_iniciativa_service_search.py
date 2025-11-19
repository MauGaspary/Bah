from datetime import date
from datetime import time as dtime

import pytest

from app.models.iniciativa_horario_model import HorarioTipo
from app.services.iniciativa_service import IniciativaService


class FakeModel:
    def encode(self, text, convert_to_numpy=True, normalize_embeddings=True):
        return [0.1, 0.2, 0.3]


class FakeRepoOK:
    def __init__(self):
        self.last_args = None

    def search_by_embedding(self, embedding, page, size):
        self.last_args = (embedding, page, size)
        item = {
            "id": "1",
            "titulo": "Título",
            "descricao": "Desc",
            "organizador_id": None,
            "link": "https://exemplo.test",
            "local": None,
            "imagem_url": "https://img.test/1.png",
            "destaque": False,
            "horarios": [
                {
                    "id": "h1",
                    "data_evento": date.today(),
                    "hora_inicio": dtime(10, 0),
                    "hora_fim": dtime(11, 0),
                    "tipo": HorarioTipo.PRESENCIAL,
                    "criado_em": None,
                }
            ],
            "criado_em": None,
            "criado_por": None,
            "editado_em": None,
            "editado_por": None,
            "organizador": None,
            "tags": [],
            "descricoes_extras": [],
        }
        return [item], 1


class FakeRepoBoom:
    def search_by_embedding(self, *a, **k):
        raise RuntimeError("falha no provedor")


def test_search_erro_sem_modelo():
    svc = IniciativaService(db=None, model=None)
    svc.repository = FakeRepoOK()
    with pytest.raises(ValueError):
        svc.search_iniciativas("café", page=1, size=10)


def test_search_sucesso():
    svc = IniciativaService(db=None, model=FakeModel())
    repo = FakeRepoOK()
    svc.repository = repo
    out = svc.search_iniciativas("café", page=2, size=5)
    assert out.total == 1 and out.filters.page == 2 and out.filters.size == 5
    assert repo.last_args[1:] == (2, 5)


def test_search_repo_explodindo_transforma_em_valueerror():
    svc = IniciativaService(db=None, model=FakeModel())
    svc.repository = FakeRepoBoom()
    with pytest.raises(ValueError):
        svc.search_iniciativas("chocolate", page=1, size=10)
