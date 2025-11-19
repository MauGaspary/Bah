from types import SimpleNamespace

import numpy as np

from app.repositories.iniciativa_repository import IniciativaRepository
from app.utils.exceptions import ResourceNotFound


class _ResEmpty:
    def mappings(self):
        return self

    def all(self):
        return []


class QueryIds:
    """Emula self.db.query(DescricoesExtras.id).filter(...).all() -> [(id,), ...]"""

    def __init__(self, ids):
        self._ids = ids

    def filter(self, *a, **k):
        return self

    def all(self):
        return [(i,) for i in self._ids]


class QueryDelete:
    """Emula self.db.query(DescricoesExtras).filter(...).delete(...)."""

    def __init__(self, ids):
        self._ids = ids
        self._deleted = 0

    def filter(self, *a, **k):
        return self

    def delete(self, **_):
        self._deleted = len(self._ids)
        return self._deleted


class QueryGeneric:
    def filter(self, *a, **k):
        return SimpleNamespace(all=lambda: [], delete=lambda **_: 0)


def test_search_by_embedding_sem_rows_retorna_vazio():
    class DB:
        def execute(self, *_a, **_k):
            return _ResEmpty()

        def query(self, *_):
            raise AssertionError("não deve consultar objetos quando sem rows")

    repo = IniciativaRepository(DB())
    itens, total = repo.search_by_embedding(np.array([0.1, 0.2]), page=1, size=10)
    assert itens == [] and total == 0


def test_get_by_id_active_404():
    class Sess:
        def query(self, *_):
            return SimpleNamespace(
                options=lambda *a, **k: SimpleNamespace(
                    filter=lambda *aa, **kk: SimpleNamespace(first=lambda: None)
                )
            )

    repo = IniciativaRepository(Sess())
    try:
        repo.get_by_id_active("X")
        assert False, "esperava ResourceNotFound"
    except ResourceNotFound:
        pass


def test_update_partial_delete_e_add(monkeypatch):
    class Sess:
        def __init__(self):
            self._added = []
            self._obj = SimpleNamespace(
                id="I", descricoes_extras=[SimpleNamespace(id="d0")]
            )

        def query(self, model):

            cls_name = getattr(model, "__name__", None) or getattr(
                getattr(model, "class_", None), "__name__", ""
            )
            is_attr = hasattr(model, "class_")
            if cls_name == "DescricoesExtras" and is_attr:
                return QueryIds(["d1", "d2"])
            if cls_name == "DescricoesExtras":
                return QueryDelete(["d1", "d2"])
            return QueryGeneric()

        def add(self, obj):
            self._added.append(obj)

        def flush(self): ...
        def commit(self): ...

    repo = IniciativaRepository(Sess())

    monkeypatch.setattr(repo, "get_by_id_active", lambda _id: repo.db._obj)

    data = {
        "descricoes_extras_delete_ids": ["d1", "d2", "d2"],
        "descricoes_extras_add": [{"descricao": "x", "descricao_vetor": [0.0]}],
    }
    out = repo.update_partial("I", data, editado_por="u")
    assert out.id == "I"


def test_create_index_if_not_exists_cria(monkeypatch):
    class Res:
        def __init__(self, v):
            self._v = v

        def scalar(self):
            return self._v

    class DB:
        def __init__(self):
            self.created = False

        def execute(self, query, *a, **k):
            txt = str(query)
            if "pg_indexes" in txt:
                return Res(False)
            if "CREATE INDEX" in txt:
                self.created = True
                return Res(None)
            return Res(None)

        def commit(self): ...

    repo = IniciativaRepository(DB())
    repo.create_index_if_not_exists()
    assert repo.db.created is True
