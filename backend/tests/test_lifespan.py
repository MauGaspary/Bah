from starlette.testclient import TestClient

import app.config.database as dbmod
from app.main import app


class DummyEngine:
    def __init__(self):
        self.disposed = False

    def dispose(self):
        self.disposed = True


def test_lifespan_startup_executes(monkeypatch):

    monkeypatch.setattr(dbmod, "engine", DummyEngine(), raising=True)

    with TestClient(app) as c:
        r = c.get("/docs")
        assert r.status_code in (200, 404, 422)


def test_different_settings(monkeypatch):
    dummy = DummyEngine()
    monkeypatch.setattr(dbmod, "engine", dummy, raising=True)

    with TestClient(app) as c:
        r = c.get("/docs")
        assert r.status_code in (200, 404, 422)

    assert dummy.disposed is True
