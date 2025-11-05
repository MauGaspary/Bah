import pytest
from fastapi import HTTPException

import app.controllers.iniciativa_controller as mod
from app.controllers.iniciativa_controller import IniciativaController
from app.utils.exceptions import ResourceNotFound


def test_listar_iniciativas_gera_500_generico(monkeypatch):
    class S:
        def __init__(self, db, model): ...
        def listar_iniciativas(self, *a, **k):
            raise RuntimeError("boom")

    monkeypatch.setattr(mod, "IniciativaService", S)
    c = IniciativaController(None, None)
    with pytest.raises(HTTPException) as exc:
        c.listar_iniciativas()
    assert exc.value.status_code == 500


def test_listar_iniciativas_gera_422(monkeypatch):
    class S:
        def __init__(self, db, model): ...
        def listar_iniciativas(self, *a, **k):
            raise ValueError("intervalo")

    monkeypatch.setattr(mod, "IniciativaService", S)
    c = IniciativaController(None, None)
    with pytest.raises(HTTPException) as exc:
        c.listar_iniciativas()
    assert exc.value.status_code == 422


def test_get_iniciativa_by_id_admin_404(monkeypatch):
    class S:
        def __init__(self, db, model): ...
        def get_iniciativa_by_id_admin(self, *_):
            raise ValueError("nao achei")

    monkeypatch.setattr(mod, "IniciativaService", S)
    c = IniciativaController(None, None)
    with pytest.raises(HTTPException) as exc:
        c.get_iniciativa_by_id_admin("X")
    assert exc.value.status_code == 404


def test_patch_iniciativa_500_generico(monkeypatch):
    class S:
        def __init__(self, db, model): ...
        def patch_iniciativa(self, *a, **k):
            raise Exception("qq coisa")

    monkeypatch.setattr(mod, "IniciativaService", S)
    c = IniciativaController(None, None)
    with pytest.raises(HTTPException) as exc:
        c.patch_iniciativa("id", payload=None)
    assert exc.value.status_code == 500


def test_patch_iniciativa_mapeia_erros(monkeypatch):
    payload = object()

    class S1:
        def __init__(self, db, model): ...
        def patch_iniciativa(self, *a, **k):
            raise ResourceNotFound("nada")

    monkeypatch.setattr(mod, "IniciativaService", S1)
    c = IniciativaController(None, None)
    with pytest.raises(HTTPException) as exc:
        c.patch_iniciativa("id", payload)
    assert exc.value.status_code == 404

    class S2:
        def __init__(self, db, model): ...
        def patch_iniciativa(self, *a, **k):
            raise ValueError("bad")

    monkeypatch.setattr(mod, "IniciativaService", S2)
    c = IniciativaController(None, None)
    with pytest.raises(HTTPException) as exc:
        c.patch_iniciativa("id", payload)
    assert exc.value.status_code == 422


def test_create_iniciativa_mapeia_erros(monkeypatch):
    class S1:
        def __init__(self, db, model): ...
        def create_iniciativa(self, *_):
            raise ValueError("bad")

    monkeypatch.setattr(mod, "IniciativaService", S1)
    c = IniciativaController(None, None)
    with pytest.raises(HTTPException) as exc:
        c.create_iniciativa(iniciativa_data=None, criado_por="u")
    assert exc.value.status_code == 422

    class S2:
        def __init__(self, db, model): ...
        def create_iniciativa(self, *_):
            raise RuntimeError("oops")

    monkeypatch.setattr(mod, "IniciativaService", S2)
    c = IniciativaController(None, None)
    with pytest.raises(HTTPException) as exc:
        c.create_iniciativa(iniciativa_data=None, criado_por="u")
    assert exc.value.status_code == 500


def test_delete_iniciativa_mapeia_erros(monkeypatch):
    class S1:
        def __init__(self, db, model): ...
        def delete_iniciativa(self, *_):
            raise ValueError("sumiu")

    monkeypatch.setattr(mod, "IniciativaService", S1)
    c = IniciativaController(None, None)
    with pytest.raises(HTTPException) as exc:
        c.delete_iniciativa("idx", "user")
    assert exc.value.status_code == 404

    class S2:
        def __init__(self, db, model): ...
        def delete_iniciativa(self, *_):
            raise RuntimeError("fail")

    monkeypatch.setattr(mod, "IniciativaService", S2)
    c = IniciativaController(None, None)
    with pytest.raises(HTTPException) as exc:
        c.delete_iniciativa("idx", "user")
    assert exc.value.status_code == 500


def test_search_iniciativas_repassa_http_exception(monkeypatch):
    class S:
        def __init__(self, db, model): ...
        def search_iniciativas(self, *_):
            raise HTTPException(status_code=418, detail="teapot")

    monkeypatch.setattr(mod, "IniciativaService", S)
    c = IniciativaController(None, None)
    with pytest.raises(HTTPException) as exc:
        c.search_iniciativas("q", 1, 10)
    assert exc.value.status_code == 418


def test_get_iniciativa_by_id_admin_falha_generica(monkeypatch):
    class S:
        def __init__(self, db, model): ...
        def get_iniciativa_by_id_admin(self, *_):
            raise RuntimeError("boom")

    monkeypatch.setattr(mod, "IniciativaService", S)
    c = IniciativaController(None, None)
    with pytest.raises(HTTPException) as exc:
        c.get_iniciativa_by_id_admin("x")
    assert exc.value.status_code == 500


def test_get_iniciativa_by_id_chama_service(monkeypatch):
    called = {}

    class S:
        def __init__(self, db, model): ...
        def get_iniciativa_by_id(self, iniciativa_id):
            called["id"] = iniciativa_id
            return "ok"

    monkeypatch.setattr(mod, "IniciativaService", S)
    c = IniciativaController(None, None)
    result = c.get_iniciativa_by_id("abc")
    assert result == "ok"
    assert called["id"] == "abc"
