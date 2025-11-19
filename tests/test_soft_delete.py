from types import SimpleNamespace

from app.repositories.iniciativa_repository import IniciativaRepository


class CaptureDB:
    def __init__(self, obj):
        self.obj = obj
        self.commits = 0
        self.refreshed = False

    def query(self, *a, **k):
        raise RuntimeError("not used")

    def commit(self):
        self.commits += 1

    def refresh(self, _):
        self.refreshed = True


def test_soft_delete_retorna_false_quando_nao_existe(monkeypatch):
    db = CaptureDB(obj=None)
    repo = IniciativaRepository(db=db)
    monkeypatch.setattr(repo, "get_by_id", lambda _id, allow_deleted=True: None)
    assert repo.soft_delete("X", "admin") is False


def test_soft_delete_marca_deletado_e_commita(monkeypatch):
    obj = SimpleNamespace(deletado_em=None, deletado_por=None)
    db = CaptureDB(obj=obj)
    repo = IniciativaRepository(db=db)
    monkeypatch.setattr(repo, "get_by_id", lambda _id, allow_deleted=True: obj)
    ok = repo.soft_delete("X", "admin")
    assert ok is True and db.commits == 1 and db.refreshed is True
    assert obj.deletado_por == "admin"
