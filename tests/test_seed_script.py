import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.scripts import seed


class DummyModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class DummyHasher:
    def hash(self, raw):
        return f"hash::{raw}"


class FakeResult:
    def __init__(self, scalar_value):
        self._scalar_value = scalar_value

    def scalar(self):
        return self._scalar_value


class FakeSeedQuery:
    def __init__(self, *, count=None, first=None, all=None, delete=None):
        self._count = self._normalize(count)
        self._first = self._normalize(first)
        self._all_queue = None
        if isinstance(all, list) and all and isinstance(all[0], list):
            self._all_queue = [list(item) for item in all]
            self._all_value = None
        else:
            self._all_value = all
        self._delete = delete

    @staticmethod
    def _normalize(value):
        if isinstance(value, list):
            return list(value)
        return value

    def _consume(self, attr):
        value = getattr(self, attr)
        if isinstance(value, list):
            if not value:
                raise AssertionError("No more values to consume")
            result = value.pop(0)
        else:
            result = value
        if isinstance(result, Exception):
            raise result
        return result

    def count(self):
        return self._consume("_count")

    def first(self):
        return self._consume("_first")

    def all(self):
        if self._all_queue is not None:
            if not self._all_queue:
                raise AssertionError("No more values to consume")
            return self._all_queue.pop(0)
        if self._all_value is None:
            return []
        return self._all_value

    def filter(self, *args, **kwargs):
        return self

    def delete(self):
        if isinstance(self._delete, Exception):
            raise self._delete
        return self._delete


class SeedSession:
    def __init__(
        self,
        *,
        execute_scalar_values=None,
        query_map=None,
        commit_exception=None,
        add_exception=None,
    ):
        self._execute_scalar_values = list(execute_scalar_values or [])
        self._query_map = query_map or {}
        self._commit_exception = commit_exception
        self._add_exception = add_exception
        self.added = []
        self.commit_calls = 0
        self.rollback_called = False
        self.closed = False
        self.flush_calls = 0

    def execute(self, stmt):
        if not self._execute_scalar_values:
            raise AssertionError("Unexpected execute call")
        value = self._execute_scalar_values.pop(0)
        return FakeResult(value)

    def query(self, model):
        key_candidates = [model, getattr(model, "__name__", None)]
        for key in key_candidates:
            if key in self._query_map:
                factory = self._query_map[key]
                if callable(factory):
                    return factory()
                return factory
        raise AssertionError(f"No query stub configured for {model}")

    def add(self, obj):
        if isinstance(self._add_exception, Exception):
            raise self._add_exception
        if callable(self._add_exception):
            self._add_exception(obj)
        self.added.append(obj)

    def commit(self):
        if self._commit_exception:
            raise self._commit_exception
        self.commit_calls += 1

    def rollback(self):
        self.rollback_called = True

    def close(self):
        self.closed = True

    def flush(self):
        self.flush_calls += 1
        if self.added:
            last = self.added[-1]
            if not hasattr(last, "id"):
                setattr(last, "id", len(self.added))

    def refresh(self, obj):

        pass


@pytest.fixture(autouse=True)
def patch_seed_dependencies(monkeypatch):
    def make_dummy(name):
        return type(f"{name}Dummy", (DummyModel,), {})

    monkeypatch.setattr(seed, "Usuario", make_dummy("Usuario"), raising=False)
    monkeypatch.setattr(seed, "Organizador", make_dummy("Organizador"), raising=False)
    monkeypatch.setattr(seed, "Tag", make_dummy("Tag"), raising=False)
    monkeypatch.setattr(seed, "Iniciativa", make_dummy("Iniciativa"), raising=False)
    monkeypatch.setattr(
        seed, "IniciativaHorario", make_dummy("IniciativaHorario"), raising=False
    )
    monkeypatch.setattr(
        seed, "IniciativaTag", make_dummy("IniciativaTag"), raising=False
    )
    monkeypatch.setattr(seed, "PasswordHasher", lambda: DummyHasher())


@pytest.fixture
def capture_seed_print(monkeypatch):
    messages = []

    def fake_print(*args, **kwargs):
        message = " ".join(str(arg) for arg in args)
        messages.append(message)

    monkeypatch.setattr(seed, "print", fake_print, raising=False)
    return messages


class ExitCalled(Exception):
    def __init__(self, code):
        super().__init__(f"exit {code}")
        self.code = code


def raise_exit(code):
    raise ExitCalled(code)


def configure_session(monkeypatch, session):
    monkeypatch.setattr(seed, "SessionLocal", lambda: session)
    return session


def test_seed_users_returns_when_existing(monkeypatch, capture_seed_print):
    session = SeedSession(query_map={seed.Usuario: lambda: FakeSeedQuery(count=3)})
    configure_session(monkeypatch, session)
    seed.seed_users()
    assert "Usuários já existem" in capture_seed_print[0]
    assert session.commit_calls == 0


def test_seed_users_creates_and_prints_credentials(monkeypatch, capture_seed_print):
    session = SeedSession(query_map={seed.Usuario: lambda: FakeSeedQuery(count=0)})
    configure_session(monkeypatch, session)
    seed.seed_users()
    assert session.commit_calls == 1
    assert len(session.added) == 3
    assert any("Credenciais de login" in message for message in capture_seed_print)


def test_seed_users_handles_exception(monkeypatch, capture_seed_print):
    session = SeedSession(
        query_map={seed.Usuario: lambda: FakeSeedQuery(count=0)},
        add_exception=RuntimeError("add fail"),
    )
    configure_session(monkeypatch, session)
    monkeypatch.setattr(seed.sys, "exit", raise_exit)
    with pytest.raises(ExitCalled):
        seed.seed_users()
    assert session.rollback_called is True
    assert "Erro ao executar seed de usuários" in capture_seed_print[-1]


def test_seed_organizadores_existing_returns(monkeypatch, capture_seed_print):
    session = SeedSession(query_map={seed.Organizador: lambda: FakeSeedQuery(count=2)})
    configure_session(monkeypatch, session)
    seed.seed_organizadores()
    assert "Organizadores já existem" in capture_seed_print[0]


def test_seed_organizadores_creates(monkeypatch):
    session = SeedSession(query_map={seed.Organizador: lambda: FakeSeedQuery(count=0)})
    configure_session(monkeypatch, session)
    seed.seed_organizadores()
    assert session.commit_calls == 1
    assert len(session.added) == 5


def test_seed_organizadores_exception(monkeypatch, capture_seed_print):
    session = SeedSession(
        query_map={seed.Organizador: lambda: FakeSeedQuery(count=0)},
        commit_exception=RuntimeError("commit fail"),
    )
    configure_session(monkeypatch, session)
    monkeypatch.setattr(seed.sys, "exit", raise_exit)
    with pytest.raises(ExitCalled):
        seed.seed_organizadores()
    assert session.rollback_called is True
    assert "Erro ao executar seed de organizadores" in capture_seed_print[-1]


def test_seed_tags_existing_returns(monkeypatch, capture_seed_print):
    session = SeedSession(query_map={seed.Tag: lambda: FakeSeedQuery(count=1)})
    configure_session(monkeypatch, session)
    seed.seed_tags()
    assert "Tags já existem" in capture_seed_print[0]


def test_seed_tags_creates(monkeypatch):
    session = SeedSession(query_map={seed.Tag: lambda: FakeSeedQuery(count=0)})
    configure_session(monkeypatch, session)
    seed.seed_tags()
    assert session.commit_calls == 1
    assert len(session.added) == 8


def test_seed_tags_exception(monkeypatch, capture_seed_print):
    session = SeedSession(
        query_map={seed.Tag: lambda: FakeSeedQuery(count=0)},
        add_exception=RuntimeError("tag fail"),
    )
    configure_session(monkeypatch, session)
    monkeypatch.setattr(seed.sys, "exit", raise_exit)
    with pytest.raises(ExitCalled):
        seed.seed_tags()
    assert session.rollback_called is True
    assert "Erro ao executar seed de tags" in capture_seed_print[-1]


def test_seed_iniciativas_existing_returns(monkeypatch, capture_seed_print):
    session = SeedSession(query_map={seed.Iniciativa: lambda: FakeSeedQuery(count=1)})
    configure_session(monkeypatch, session)
    seed.seed_iniciativas()
    assert "Iniciativas já existem" in capture_seed_print[0]


def test_seed_iniciativas_requires_usuario(monkeypatch, capture_seed_print):
    session = SeedSession(
        query_map={
            seed.Iniciativa: lambda: FakeSeedQuery(count=0),
            seed.Usuario: lambda: FakeSeedQuery(first=None),
        }
    )
    configure_session(monkeypatch, session)
    seed.seed_iniciativas()
    assert "Nenhum usuário encontrado" in capture_seed_print[-1]


def test_seed_iniciativas_requires_organizadores(monkeypatch, capture_seed_print):
    session = SeedSession(
        query_map={
            seed.Iniciativa: lambda: FakeSeedQuery(count=0),
            seed.Usuario: lambda: FakeSeedQuery(first=SimpleNamespace(id=1)),
            seed.Organizador: lambda: FakeSeedQuery(all=[]),
        }
    )
    configure_session(monkeypatch, session)
    seed.seed_iniciativas()
    assert "Nenhum organizador encontrado" in capture_seed_print[-1]


def test_seed_iniciativas_requires_tags(monkeypatch, capture_seed_print):
    session = SeedSession(
        query_map={
            seed.Iniciativa: lambda: FakeSeedQuery(count=0),
            seed.Usuario: lambda: FakeSeedQuery(first=SimpleNamespace(id=1)),
            seed.Organizador: lambda: FakeSeedQuery(all=[SimpleNamespace(id=1)]),
            seed.Tag: lambda: FakeSeedQuery(all=[]),
        }
    )
    configure_session(monkeypatch, session)
    seed.seed_iniciativas()
    assert "Nenhuma tag encontrada" in capture_seed_print[-1]


def test_seed_iniciativas_success(monkeypatch):
    usuario = SimpleNamespace(id=10)
    organizadores = [SimpleNamespace(id=i) for i in range(1, 6)]
    tags = [
        SimpleNamespace(id=i, nome=nome)
        for i, nome in enumerate(
            [
                "Meio Ambiente",
                "Educação",
                "Saúde",
                "Tecnologia",
                "Cultura",
                "Esporte",
                "Inclusão Social",
                "Desenvolvimento Sustentável",
            ],
            start=1,
        )
    ]
    session = SeedSession(
        query_map={
            seed.Iniciativa: lambda: FakeSeedQuery(count=0),
            seed.Usuario: lambda: FakeSeedQuery(first=usuario),
            seed.Organizador: lambda: FakeSeedQuery(all=organizadores),
            seed.Tag: lambda: FakeSeedQuery(all=tags),
        }
    )
    configure_session(monkeypatch, session)
    seed.seed_iniciativas()
    assert session.commit_calls == 1
    assert session.flush_calls >= 1
    assert any(isinstance(obj, DummyModel) for obj in session.added)
    assert session.closed is True


def test_seed_iniciativas_exception(monkeypatch, capture_seed_print):
    usuario = SimpleNamespace(id=1)
    organizadores = [SimpleNamespace(id=1)]
    tags = [SimpleNamespace(id=1, nome="Meio Ambiente")]
    session = SeedSession(
        query_map={
            seed.Iniciativa: lambda: FakeSeedQuery(count=0),
            seed.Usuario: lambda: FakeSeedQuery(first=usuario),
            seed.Organizador: lambda: FakeSeedQuery(all=organizadores),
            seed.Tag: lambda: FakeSeedQuery(all=tags),
        },
        commit_exception=RuntimeError("commit boom"),
    )
    configure_session(monkeypatch, session)
    monkeypatch.setattr(seed.sys, "exit", raise_exit)
    with pytest.raises(ExitCalled):
        seed.seed_iniciativas()
    assert session.rollback_called is True
    assert "Erro ao executar seed de iniciativas" in capture_seed_print[-1]


def test_seed_main_invocation(monkeypatch):
    calls = []

    def fake_seed(name):
        calls.append(name)

    namespace = {
        "__name__": "__main__",
        "seed_users": lambda: fake_seed("users"),
        "seed_organizadores": lambda: fake_seed("organizadores"),
        "seed_tags": lambda: fake_seed("tags"),
        "seed_iniciativas": lambda: fake_seed("iniciativas"),
        "print": lambda *args, **kwargs: None,
    }

    source = Path(seed.__file__).read_text(encoding="utf-8")
    module_ast = ast.parse(source, filename=seed.__file__)
    main_if = next(
        node
        for node in module_ast.body
        if isinstance(node, ast.If)
        and isinstance(node.test, ast.Compare)
        and isinstance(node.test.left, ast.Name)
        and node.test.left.id == "__name__"
        and node.test.comparators
        and isinstance(node.test.comparators[0], ast.Constant)
        and node.test.comparators[0].value == "__main__"
    )
    ast.fix_missing_locations(main_if)
    exec(
        compile(ast.Module(body=[main_if], type_ignores=[]), seed.__file__, "exec"),
        namespace,
    )

    assert set(calls) == {"users", "organizadores", "tags", "iniciativas"}
