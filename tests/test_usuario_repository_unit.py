from types import SimpleNamespace

import pytest

from app.repositories.usuario_repository import UsuarioRepository


class FakeScalarResult:
    def __init__(self, values):
        self._values = list(values)

    def scalars(self):
        return self

    def first(self):
        return self._values[0] if self._values else None


class FakeQuery:
    def __init__(self, delete_value=0):
        self._delete_value = delete_value

    def filter(self, *args, **kwargs):
        return self

    def delete(self):
        if isinstance(self._delete_value, Exception):
            raise self._delete_value
        return self._delete_value


class FakeSession:
    def __init__(self, execute_results=None, query_results=None):
        self._execute_results = list(execute_results or [])
        self._query_results = list(query_results or [])
        self.added = []
        self.commits = 0
        self.refreshes = []
        self.rollbacks = 0

    def execute(self, stmt):
        if not self._execute_results:
            raise AssertionError("Unexpected execute call")
        return self._execute_results.pop(0)

    def query(self, model):
        if not self._query_results:
            raise AssertionError("Unexpected query call")
        result = self._query_results.pop(0)
        if callable(result):
            return result(model)
        return result

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self.commits += 1

    def refresh(self, obj):
        self.refreshes.append(obj)

    def rollback(self):
        self.rollbacks += 1


class DummyUsuario:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class DummyHasher:
    def hash(self, raw):
        return f"hashed::{raw}"


def test_get_by_email_returns_user(monkeypatch):
    fake_user = SimpleNamespace(email="user@example.com")
    session = FakeSession(execute_results=[FakeScalarResult([fake_user])])
    repo = UsuarioRepository(session)
    assert repo.get_by_email("user@example.com") is fake_user


def test_email_exists_true(monkeypatch):
    session = FakeSession(execute_results=[FakeScalarResult([object()])])
    repo = UsuarioRepository(session)
    assert repo.email_exists("exists@example.com") is True


def test_email_exists_false(monkeypatch):
    session = FakeSession(execute_results=[FakeScalarResult([])])
    repo = UsuarioRepository(session)
    assert repo.email_exists("missing@example.com") is False


def test_create_trims_email_and_commits(monkeypatch):
    session = FakeSession()
    monkeypatch.setattr(
        "app.repositories.usuario_repository.PasswordHasher", lambda: DummyHasher()
    )
    monkeypatch.setattr(
        "app.repositories.usuario_repository.Usuario", DummyUsuario, raising=False
    )
    repo = UsuarioRepository(session)
    created = repo.create(
        SimpleNamespace(
            email="  new@example.com  ",
            password="secret",
            nome="Name",
            sobrenome="Surname",
        )
    )
    assert isinstance(created, DummyUsuario)
    assert created.email == "new@example.com"
    assert created.senha_hash == "hashed::secret"
    assert session.added == [created]
    assert session.commits == 1
    assert session.refreshes == [created]


def test_get_by_id_returns_user():
    fake_user = SimpleNamespace(id="123")
    session = FakeSession(execute_results=[FakeScalarResult([fake_user])])
    repo = UsuarioRepository(session)
    assert repo.get_by_id("123") is fake_user


def test_delete_existing_user_commits():
    session = FakeSession(query_results=[FakeQuery(delete_value=1)])
    repo = UsuarioRepository(session)
    assert repo.delete("abc") is True
    assert session.commits == 1


def test_delete_missing_user_returns_false():
    session = FakeSession(query_results=[FakeQuery(delete_value=0)])
    repo = UsuarioRepository(session)
    assert repo.delete("missing") is False
    assert session.commits == 0


def test_delete_raises_exception_and_rolls_back():
    session = FakeSession(query_results=[FakeQuery(delete_value=RuntimeError("boom"))])
    repo = UsuarioRepository(session)
    with pytest.raises(RuntimeError):
        repo.delete("err")
    assert session.rollbacks == 1
