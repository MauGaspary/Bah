import pytest
from fastapi import HTTPException

import app.controllers.usuario_controller as controller_mod
from app.controllers.usuario_controller import UsuarioController


def test_delete_usuario_mapeia_excecoes(monkeypatch):
    class RepoValueError:
        def __init__(self, db): ...

        def delete_usuario(self, *_):
            raise ValueError("missing")

    monkeypatch.setattr(controller_mod, "UsuarioService", RepoValueError)
    controller = UsuarioController(db=None)
    with pytest.raises(HTTPException) as excinfo:
        controller.delete_usuario("abc")
    assert excinfo.value.status_code == 404

    class RepoRuntimeError:
        def __init__(self, db): ...

        def delete_usuario(self, *_):
            raise RuntimeError("fail")

    monkeypatch.setattr(controller_mod, "UsuarioService", RepoRuntimeError)
    controller = UsuarioController(db=None)
    with pytest.raises(HTTPException) as excinfo:
        controller.delete_usuario("abc")
    assert excinfo.value.status_code == 500


def test_delete_usuario_success(monkeypatch):
    class Repo:
        def __init__(self, db): ...

        def delete_usuario(self, usuario_id):
            self.last = usuario_id
            return True

    repo = Repo(None)
    monkeypatch.setattr(controller_mod, "UsuarioService", lambda db: repo)
    controller = UsuarioController(db=None)
    assert controller.delete_usuario("u123") is True
    assert repo.last == "u123"


def test_get_usuario_by_id_404(monkeypatch):
    class Repo:
        def __init__(self, db): ...

        def get_usuario_by_id(self, *_):
            raise ValueError("missing")

    monkeypatch.setattr(controller_mod, "UsuarioService", Repo)
    controller = UsuarioController(db=None)
    with pytest.raises(HTTPException) as excinfo:
        controller.get_usuario_by_id("x")
    assert excinfo.value.status_code == 404


def test_get_usuario_by_id_success(monkeypatch):
    class Repo:
        def __init__(self, db): ...

        def get_usuario_by_id(self, usuario_id):
            return {"id": usuario_id}

    monkeypatch.setattr(controller_mod, "UsuarioService", Repo)
    controller = UsuarioController(db=None)
    assert controller.get_usuario_by_id("id1") == {"id": "id1"}
