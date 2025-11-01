import pytest

from app.repositories.iniciativa_repository import IniciativaRepository
from app.utils.exceptions import ResourceNotFound


class FakeQueryNotFound:
    def filter(self, *a, **k):
        return self

    def first(self):
        return None

    def all(self):
        return []

    def delete(self, *a, **k):
        return 0


class FakeSession:
    def __init__(self):
        self._last_added = []

    def query(self, model):
        return FakeQueryNotFound()

    def add(self, obj):
        self._last_added.append(obj)

    def flush(self): ...
    def commit(self): ...
    def refresh(self, _obj=None): ...


def test_update_partial_descricoes_update_id_inexistente_gera_404(monkeypatch):
    db = FakeSession()
    repo = IniciativaRepository(db=db)

    class FakeObj:
        id = "I1"
        descricoes_extras = []

    monkeypatch.setattr(repo, "get_by_id_active", lambda _id: FakeObj())
    data = {"descricoes_extras_update": [{"id": "DZZ", "descricao": "novo texto"}]}
    with pytest.raises(ResourceNotFound):
        repo.update_partial("I1", data, editado_por="user")
