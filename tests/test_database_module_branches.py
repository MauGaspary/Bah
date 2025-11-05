import importlib
from types import SimpleNamespace

import sqlalchemy

import app.config.database as database


def test_create_engine_usando_connect_args_para_postgresql(monkeypatch):
    calls = {}

    def fake_create_engine(url, **kwargs):
        calls["url"] = url
        calls["connect_args"] = kwargs.get("connect_args")
        return SimpleNamespace()

    monkeypatch.setattr(sqlalchemy, "create_engine", fake_create_engine)
    monkeypatch.setenv("DATABASE_URL", "PostgreSQL+psycopg2://user:pass@host/db")
    importlib.reload(database)
    assert calls["connect_args"] == {"check_same_thread": False}


def test_get_db_fecha_sessao(monkeypatch):
    closed = {"v": False}

    class FakeSess:
        def close(self):
            closed["v"] = True

    monkeypatch.setattr(database, "SessionLocal", lambda: FakeSess())
    gen = database.get_db()
    sess = next(gen)
    assert isinstance(sess, FakeSess.__class__) or sess is not None
    try:
        next(gen)
    except StopIteration:
        pass
    assert closed["v"] is True
