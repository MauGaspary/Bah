from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.services.usuario_service import UsuarioService
from app.utils.exceptions import EmailAlreadyExistsException


def _make_service(repo):
    service = object.__new__(UsuarioService)
    service.repository = repo
    return service


def test_create_user_valida_email(monkeypatch):
    class Repo:
        def get_by_email(self, email):
            return None

        def create(self, data):
            return SimpleNamespace(
                id="1",
                nome=data.nome,
                sobrenome=data.sobrenome,
                email=data.email,
                criado_em=None,
                criado_por=None,
                editado_em=None,
                editado_por=None,
            )

    service = _make_service(Repo())
    user_data = SimpleNamespace(
        nome="Nome",
        sobrenome="Sobrenome",
        email="user@example.com",
        password="segredo",
    )
    response = service.create_user(user_data)
    assert response.email == "user@example.com"


def test_create_user_formato_email_invalido():
    repo = SimpleNamespace(get_by_email=lambda email: None)
    service = _make_service(repo)
    bad_data = SimpleNamespace(
        nome="Nome",
        sobrenome="Sobrenome",
        email="not-an-email",
        password="segredo",
    )
    with pytest.raises(ValueError):
        service.create_user(bad_data)


def test_create_user_email_duplicado():
    repo = SimpleNamespace(get_by_email=lambda email: object())
    service = _make_service(repo)
    data = SimpleNamespace(
        nome="Nome",
        sobrenome="Sobrenome",
        email="dup@example.com",
        password="segredo",
    )
    with pytest.raises(EmailAlreadyExistsException):
        service.create_user(data)


def test_create_user_erro_interno():
    class Repo:
        def get_by_email(self, email):
            return None

        def create(self, data):
            raise RuntimeError("db down")

    service = _make_service(Repo())
    data = SimpleNamespace(
        nome="Nome",
        sobrenome="Sobrenome",
        email="user@example.com",
        password="segredo",
    )
    with pytest.raises(HTTPException) as excinfo:
        service.create_user(data)
    assert excinfo.value.status_code == 500


def test_delete_usuario_fluxos():
    class Repo:
        def __init__(self):
            self.existing = {"ok": object(), "fail": object()}
            self.deleted = False

        def get_by_id(self, user_id):
            return self.existing.get(user_id)

        def delete(self, user_id):
            if user_id == "fail":
                return False
            self.deleted = True
            return True

    repo = Repo()
    service = _make_service(repo)
    with pytest.raises(ValueError):
        service.delete_usuario("missing")

    with pytest.raises(RuntimeError):
        service.delete_usuario("fail")

    assert service.delete_usuario("ok") is True
    assert repo.deleted is True


def test_get_usuario_by_id_fluxos():
    class Repo:
        def __init__(self):
            self.existing = {
                "user": SimpleNamespace(
                    id="user",
                    nome="Nome",
                    sobrenome="Sobrenome",
                    email="user@example.com",
                    senha="hash",
                    criado_em=None,
                    criado_por=None,
                )
            }

        def get_by_id(self, user_id):
            return self.existing.get(user_id)

    repo = Repo()
    service = _make_service(repo)
    with pytest.raises(ValueError):
        service.get_usuario_by_id("missing")

    response = service.get_usuario_by_id("user")
    assert response.id == "user"
