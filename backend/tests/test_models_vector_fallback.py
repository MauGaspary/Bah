import builtins
import importlib
import sys

import pytest


@pytest.fixture
def restore_module():
    original = sys.modules.get("app.models.descricoes_extras_model")
    original_iniciativa = sys.modules.get("app.models.iniciativa_model")
    try:
        yield
    finally:
        if original is not None:
            sys.modules["app.models.descricoes_extras_model"] = original
        else:
            sys.modules.pop("app.models.descricoes_extras_model", None)
        if original_iniciativa is not None:
            sys.modules["app.models.iniciativa_model"] = original_iniciativa
        else:
            sys.modules.pop("app.models.iniciativa_model", None)


def _force_import_error(monkeypatch):
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "pgvector.sqlalchemy":
            raise ImportError("pgvector not installed")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)


def test_descricoes_extras_vector_fallback(monkeypatch, restore_module):
    from sqlalchemy.orm import declarative_base

    import app.models.base as base_mod

    original_base = base_mod.Base
    monkeypatch.setattr(base_mod, "Base", declarative_base())
    _force_import_error(monkeypatch)
    sys.modules.pop("app.models.descricoes_extras_model", None)
    module = importlib.import_module("app.models.descricoes_extras_model")
    from sqlalchemy import Text

    assert module.VectorType is Text
    monkeypatch.setattr(base_mod, "Base", original_base, raising=False)


def test_iniciativa_model_vector_fallback(monkeypatch, restore_module):
    from sqlalchemy.orm import declarative_base

    import app.models.base as base_mod

    original_base = base_mod.Base
    monkeypatch.setattr(base_mod, "Base", declarative_base())
    _force_import_error(monkeypatch)
    sys.modules.pop("app.models.iniciativa_model", None)
    module = importlib.import_module("app.models.iniciativa_model")
    from sqlalchemy import Text

    assert module.VectorType is Text
    monkeypatch.setattr(base_mod, "Base", original_base, raising=False)
