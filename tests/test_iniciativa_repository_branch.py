from datetime import date, datetime, time
from types import SimpleNamespace

import pytest

from app.models.descricoes_extras_model import DescricoesExtras
from app.models.iniciativa_horario_model import HorarioTipo, IniciativaHorario
from app.models.iniciativa_model import Iniciativa
from app.models.tag_model import Tag
from app.repositories.iniciativa_repository import IniciativaRepository
from app.utils.exceptions import ResourceNotFound


class FakeQuery:
    def __init__(self, *, first=None, all=None, delete_result=0):
        self._first = first
        self._all = all
        self._delete_result = delete_result
        self.deleted = False
        self.filter_calls = 0

    def options(self, *args, **kwargs):
        return self

    def join(self, *args, **kwargs):
        return self

    def filter(self, *args, **kwargs):
        self.filter_calls += 1
        return self

    def where(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def offset(self, *args, **kwargs):
        return self

    def limit(self, *args, **kwargs):
        return self

    def delete(self, synchronize_session=False):
        self.deleted = True
        return self._delete_result

    def first(self):
        return self._first

    def all(self):
        return self._all


class FakeScalars:
    def __init__(self, values):
        self._values = values

    def all(self):
        return self._values


class FakeMappings:
    def __init__(self, rows):
        self._rows = rows

    def all(self):
        return list(self._rows)


class FakeExecuteResult:
    def __init__(self, *, scalars=None, mappings=None, fetchall=None):
        self._scalars = scalars
        self._mappings = mappings
        self._fetchall = fetchall

    def scalars(self):
        return FakeScalars(self._scalars or [])

    def mappings(self):
        return FakeMappings(self._mappings or [])

    def fetchall(self):
        return self._fetchall or []


class FakeScalarResult:
    def __init__(self, value):
        self._value = value

    def scalar(self):
        return self._value


class FakeSession:
    def __init__(self, query_map=None, execute_results=None):
        self.query_map = query_map or {}
        self.execute_results = list(execute_results or [])
        self.added = []
        self.committed = False
        self.flushed = 0
        self.refreshed = []
        self.executed_queries = []

    def query(self, model):
        value = self.query_map.get(model)
        if value is None:
            raise AssertionError(f"Unexpected query for {model}")
        if callable(value):
            return value()
        return value

    def add(self, obj):
        self.added.append(obj)

    def flush(self):
        self.flushed += 1

    def commit(self):
        self.committed = True

    def refresh(self, obj):
        self.refreshed.append(obj)

    def execute(self, *args, **kwargs):
        self.executed_queries.append((args, kwargs))
        if not self.execute_results:
            raise AssertionError("Unexpected execute call")
        result = self.execute_results.pop(0)
        if callable(result):
            return result(*args, **kwargs)
        return result


def _sample_iniciativa_data():
    horario = SimpleNamespace(
        data_evento=date(2025, 1, 1),
        hora_inicio=time(9, 0),
        hora_fim=time(10, 0),
        tipo=HorarioTipo.PRESENCIAL,
    )
    return SimpleNamespace(
        titulo="Titulo",
        descricao="Descricao",
        descricoes_extras=["extra"],
        organizador_id="org",
        link="https://example.com",
        local="Local",
        imagem_url="https://example.com/img.png",
        destaque=True,
        horarios=[horario],
        tag_ids=["tag1"],
    )


def test_iniciativa_repository_create_popula_relacionamentos(monkeypatch):
    session = FakeSession()
    repo = IniciativaRepository(session)

    created = SimpleNamespace(id="novo")
    monkeypatch.setattr(repo, "get_by_id", lambda _id: created)

    iniciativa_data = _sample_iniciativa_data()
    vetor = [0.1, 0.2]
    extras_vetores = [[0.3, 0.4]]

    result = repo.create(iniciativa_data, "criador", vetor, extras_vetores)

    assert result is created

    assert len(session.added) == 4
    assert session.committed is True
    assert session.refreshed and session.flushed == 1


def test_iniciativa_repository_create_erro_recuperar(monkeypatch):
    session = FakeSession()
    repo = IniciativaRepository(session)
    monkeypatch.setattr(repo, "get_by_id", lambda _id: None)
    with pytest.raises(ValueError):
        repo.create(_sample_iniciativa_data(), "u", [0.1], [[0.2]])


def test_iniciativa_repository_list_iniciativas_filtros():
    session = FakeSession(
        execute_results=[FakeExecuteResult(scalars=[SimpleNamespace(id="i1")])]
    )
    repo = IniciativaRepository(session)
    items = repo.list_iniciativas(
        q="busca",
        created_from=datetime(2024, 1, 1),
        created_to=datetime(2024, 1, 31),
        order_dir="asc",
    )
    assert isinstance(items, list)


def test_iniciativa_repository_count_iniciativas():
    session = FakeSession(execute_results=[FakeScalarResult(5)])
    repo = IniciativaRepository(session)
    total = repo.count_iniciativas(
        q="busca",
        created_from=datetime(2024, 1, 1),
        created_to=datetime(2024, 1, 31),
    )
    assert total == 5


def test_iniciativa_repository_update_partial_fluxo(monkeypatch):
    existing_extra = SimpleNamespace(
        id="extra1", descricao="old", descricao_vetor=[0.0]
    )
    objeto = SimpleNamespace(
        id="init",
        titulo="Titulo",
        descricao="Descricao",
        link="https://example.com",
        destaque=False,
        local="Local",
        imagem_url="https://example.com/img.png",
        organizador_id="org",
        tags=[],
        descricoes_extras=[existing_extra],
        editado_em=None,
        editado_por=None,
    )

    session = FakeSession(
        query_map={
            Tag: FakeQuery(all=[SimpleNamespace(id="tag1")]),
            IniciativaHorario: FakeQuery(delete_result=1),
            DescricoesExtras: FakeQuery(first=existing_extra),
            DescricoesExtras.id: FakeQuery(all=[("extra1",)]),
        }
    )
    repo = IniciativaRepository(session)
    monkeypatch.setattr(repo, "get_by_id_active", lambda _id: objeto)
    monkeypatch.setattr(repo, "get_by_id", lambda _id, allow_deleted=False: objeto)

    data = {
        "titulo": "Novo",
        "descricao": "Outra",
        "link": "https://novo",
        "destaque": True,
        "local": "Novo Local",
        "imagem_url": "https://img",
        "organizador_id": "org",
        "tags_ids": ["tag1"],
        "horarios": [
            {
                "data_evento": date(2025, 1, 2),
                "hora_inicio": time(8, 0),
                "hora_fim": time(9, 0),
                "tipo": HorarioTipo.ONLINE,
            }
        ],
        "descricoes_extras_update": [
            {"descricao": "sem id"},
            {"id": "extra1", "descricao": "nova", "descricao_vetor": [1.0]},
        ],
        "descricoes_extras_delete_ids": ["extra1"],
        "descricoes_extras_add": [
            {"descricao": "adicional", "descricao_vetor": [0.5]},
            {"descricao": "", "descricao_vetor": None},
        ],
    }

    result = repo.update_partial("init", data=data, editado_por="editor", model=None)
    assert result is objeto
    assert objeto.titulo == "Novo"
    assert objeto.editado_por == "editor"
    assert session.committed is True
    assert any(isinstance(item, IniciativaHorario) for item in session.added)


def test_iniciativa_repository_update_partial_extra_inexistente(monkeypatch):
    session = FakeSession(query_map={DescricoesExtras: FakeQuery(first=None)})
    repo = IniciativaRepository(session)
    monkeypatch.setattr(repo, "get_by_id_active", lambda _id: SimpleNamespace(id="i"))
    with pytest.raises(ResourceNotFound):
        repo.update_partial(
            "i",
            data={"descricoes_extras_update": [{"id": "missing", "descricao": "nova"}]},
        )


def test_iniciativa_repository_update_partial_delete_ids_inexistente(monkeypatch):
    session = FakeSession(query_map={DescricoesExtras.id: FakeQuery(all=[])})
    repo = IniciativaRepository(session)
    monkeypatch.setattr(
        repo,
        "get_by_id_active",
        lambda _id: SimpleNamespace(id="i", descricoes_extras=[]),
    )
    with pytest.raises(ResourceNotFound):
        repo.update_partial(
            "i",
            data={"descricoes_extras_delete_ids": ["not-found"]},
        )


def test_iniciativa_repository_soft_delete(monkeypatch):
    iniciativa = SimpleNamespace(id="i", deletado_em=None, deletado_por=None)
    repo = IniciativaRepository(None)
    monkeypatch.setattr(repo, "get_by_id", lambda _id, allow_deleted: iniciativa)
    repo.db = SimpleNamespace(commit=lambda: None, refresh=lambda obj: None)
    assert repo.soft_delete("i", "user") is True
    assert iniciativa.deletado_por == "user"


def test_iniciativa_repository_soft_delete_inexistente(monkeypatch):
    repo = IniciativaRepository(None)
    monkeypatch.setattr(repo, "get_by_id", lambda *_, **__: None)
    assert repo.soft_delete("missing", "user") is False


def test_iniciativa_repository_check_conflicting_horarios():
    horario = SimpleNamespace(
        data_evento=date(2025, 1, 1),
        hora_inicio=time(9, 0),
        hora_fim=time(10, 0),
    )
    fake_conflict = SimpleNamespace()

    query = FakeQuery(all=[fake_conflict])
    session = FakeSession(query_map={IniciativaHorario: query})
    repo = IniciativaRepository(session)
    conflitos = repo.check_conflicting_horarios(
        "org", [horario], exclude_iniciativa_id="ignore"
    )
    assert conflitos == [fake_conflict]


def test_iniciativa_repository_search_by_embedding_sem_resultado():
    session = FakeSession(execute_results=[FakeExecuteResult(mappings=[])])
    repo = IniciativaRepository(session)
    itens, total = repo.search_by_embedding([0.1, 0.2], page=1, size=10)
    assert itens == [] and total == 0


def test_iniciativa_repository_check_duplicate_exclude():
    query = FakeQuery(first=None)
    session = FakeSession(query_map={Iniciativa: query})
    repo = IniciativaRepository(session)
    repo.check_duplicate_iniciativa("titulo", "org", exclude_id="ignore")
    assert query.filter_calls >= 2


def test_iniciativa_repository_search_by_embedding_com_resultado():
    rows = [
        {"id": "1", "best_sim": None, "total_count": 2, "titulo": "A"},
        {"id": "2", "best_sim": 0.5, "total_count": 2, "titulo": "B"},
    ]
    session = FakeSession(
        execute_results=[FakeExecuteResult(mappings=rows)],
        query_map={
            Iniciativa: FakeQuery(
                all=[SimpleNamespace(id="1"), SimpleNamespace(id="2")]
            )
        },
    )
    repo = IniciativaRepository(session)
    itens, total = repo.search_by_embedding([0.1], page=1, size=10)
    assert total == 2
    assert [item.id for item in itens] == ["1", "2"]


def test_iniciativa_repository_create_index_if_not_exists():
    session = FakeSession(execute_results=[FakeScalarResult(False), object()])
    repo = IniciativaRepository(session)
    repo.create_index_if_not_exists()
    assert len(session.executed_queries) == 2
