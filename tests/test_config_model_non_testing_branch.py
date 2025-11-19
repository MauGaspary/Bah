from starlette.applications import Starlette
from starlette.requests import Request

from app.config.model import get_embedding_model


def test_get_embedding_model_returns_app_state_when_not_testing(monkeypatch):

    monkeypatch.setenv("TESTING", "false")

    app = Starlette()
    sentinel = object()
    app.state.embedding_model = sentinel

    req = Request({"type": "http", "app": app})
    assert get_embedding_model(req) is sentinel
