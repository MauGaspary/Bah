import importlib
import sys
import types

from starlette.testclient import TestClient


def test_create_app_sets_embedding_when_not_testing(monkeypatch):

    monkeypatch.setenv("TESTING", "false")

    fake_mod = types.SimpleNamespace()

    class DummyST:
        def __init__(self, name):
            self.name = name

    fake_mod.SentenceTransformer = DummyST
    monkeypatch.setitem(sys.modules, "sentence_transformers", fake_mod)

    import app.config.database as dbmod

    class DummyEngine:
        def dispose(self):
            pass

    monkeypatch.setattr(dbmod, "engine", DummyEngine(), raising=True)

    import app.main as main

    importlib.reload(main)

    app = main.create_app()
    assert hasattr(app.state, "embedding_model")
    assert isinstance(app.state.embedding_model, DummyST)

    with TestClient(app) as c:
        r = c.get("/")
        assert r.status_code in (200, 307, 308)
