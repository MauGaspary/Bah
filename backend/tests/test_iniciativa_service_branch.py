from datetime import date, datetime, timedelta
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.services.iniciativa_service import IniciativaService


def _make_service(repo=None, model=None):
    service = object.__new__(IniciativaService)
    service.repository = repo or SimpleNamespace(
        list_iniciativas=lambda *args, **kwargs: [],
        count_iniciativas=lambda *args, **kwargs: 0,
    )
    service.model = model
    return service


def test_listar_iniciativas_valida_intervalo_datas():
    service = _make_service()
    start = datetime(2024, 1, 10)
    end = datetime(2024, 1, 5)
    with pytest.raises(ValueError):
        service.listar_iniciativas(created_from=start, created_to=end)


def test_listar_iniciativas_order_by_fallback():
    captured = {}

    class Repo:
        def list_iniciativas(self, *args, **kwargs):
            captured["order_by"] = args[3] if len(args) > 3 else None
            return []

        def count_iniciativas(self, *args, **kwargs):
            return 0

    service = _make_service(repo=Repo())
    service.listar_iniciativas(order_by="invalido")
    assert captured["order_by"] == "criado_em"


def test_patch_iniciativa_exige_model_para_update():
    service = _make_service(repo=SimpleNamespace())
    payload = SimpleNamespace(
        model_dump=lambda **kwargs: {
            "descricoes_extras_update": [{"id": "1", "descricao": "texto"}]
        }
    )
    with pytest.raises(ValueError):
        service.patch_iniciativa("id", payload, model=None)


def test_patch_iniciativa_exige_model_para_add():
    service = _make_service(repo=SimpleNamespace())
    payload = SimpleNamespace(
        model_dump=lambda **kwargs: {"descricoes_extras_add": ["nova descricao"]}
    )
    with pytest.raises(ValueError):
        service.patch_iniciativa("id", payload, model=None)


def test_patch_iniciativa_processa_descricoes(monkeypatch):
    encoded = []

    class Model:
        def encode(self, texto, **kwargs):
            encoded.append(texto)
            return [0.1, 0.2]

    updated_payload = {}

    class Repo:
        def get_by_id_active(self, iniciativa_id):
            return SimpleNamespace(
                id=iniciativa_id,
                tags=[],
                descricoes_extras=[],
            )

        def update_partial(self, **kwargs):
            updated_payload.update(kwargs["data"])
            return SimpleNamespace(id="id", titulo="t")

    service = _make_service(repo=Repo(), model=Model())
    monkeypatch.setattr(
        "app.services.iniciativa_service.IniciativaSchema.model_validate",
        staticmethod(lambda obj: obj),
        raising=False,
    )

    payload = SimpleNamespace(
        model_dump=lambda **kwargs: {
            "descricoes_extras_update": [
                {"id": "1"},
                {"id": "2", "descricao": "Texto novo"},
            ],
            "descricoes_extras_add": ["Outra descrição"],
        }
    )

    result = service.patch_iniciativa("id", payload, model=service.model)
    assert result.id == "id"

    assert "descricao_vetor" not in updated_payload["descricoes_extras_update"][0]
    assert encoded


def _sample_iniciativa_data(**overrides):
    base = {
        "titulo": "Titulo",
        "descricao": "Descricao",
        "descricoes_extras": [],
        "organizador_id": "org-1",
        "link": "https://example.com",
        "local": "Local",
        "imagem_url": "https://example.com/img.jpg",
        "destaque": False,
        "horarios": [],
        "tag_ids": [],
    }
    base.update(overrides)
    return SimpleNamespace(**base)


def test_create_iniciativa_exige_organizador():
    service = _make_service(repo=SimpleNamespace())
    data = _sample_iniciativa_data(organizador_id=None)
    with pytest.raises(ValueError):
        service.create_iniciativa(data, criado_por="sistema")


def test_create_iniciativa_error_constraint():
    class Repo:
        db = SimpleNamespace()

        def organizador_exists(self, organizador_id):
            return True

        def tags_exist(self, tag_ids):
            return tag_ids

        def check_duplicate_iniciativa(self, *args, **kwargs):
            return None

        def check_conflicting_horarios(self, *a, **k):
            return []

        def create(self, *args, **kwargs):
            raise RuntimeError("violates CHECK constraint")

    class Model:
        def encode(self, texto, **kwargs):
            return [0.1, 0.2, 0.3]

    service = _make_service(repo=Repo(), model=Model())
    data = _sample_iniciativa_data()
    with pytest.raises(ValueError):
        service.create_iniciativa(data, criado_por="sistema")


def test_get_iniciativa_by_id_retorna_404():
    repo = SimpleNamespace(get_by_id=lambda iniciativa_id, allow_deleted=False: None)
    service = _make_service(repo=repo)
    with pytest.raises(HTTPException) as excinfo:
        service.get_iniciativa_by_id("nao-existe")
    assert excinfo.value.status_code == 404


def test_get_calendario_mensal_repassa_excecao():
    def raise_error(*args, **kwargs):
        raise RuntimeError("db error")

    repo = SimpleNamespace(
        get_horarios_do_mes=raise_error,
        get_tags_por_iniciativa=lambda rows: {},
    )
    service = _make_service(repo=repo)
    with pytest.raises(RuntimeError):
        service.get_calendario_mensal(date(2024, 1, 1))


def test_get_iniciativa_by_id_sucesso(monkeypatch):
    iniciativa = SimpleNamespace(id="ok")
    repo = SimpleNamespace(
        get_by_id=lambda iniciativa_id, allow_deleted=False: iniciativa
    )
    service = _make_service(repo=repo)
    monkeypatch.setattr(
        "app.services.iniciativa_service.IniciativaResponse.model_validate",
        staticmethod(lambda obj: obj),
        raising=False,
    )
    result = service.get_iniciativa_by_id("ok")
    assert result is iniciativa


def test_search_iniciativas_sem_modelo_disponivel():
    service = _make_service(repo=SimpleNamespace(), model=None)
    with pytest.raises(ValueError):
        service.search_iniciativas("busca", 1, 10)


def test_search_iniciativas_propaga_erro_repo():
    class Model:
        def encode(self, texto, **kwargs):
            return [0.5]

    def failing_search(*args, **kwargs):
        raise RuntimeError("falha no banco")

    repo = SimpleNamespace(search_by_embedding=failing_search)
    service = _make_service(repo=repo, model=Model())
    with pytest.raises(ValueError) as excinfo:
        service.search_iniciativas("busca", 1, 10)
    assert "falha" in str(excinfo.value)
