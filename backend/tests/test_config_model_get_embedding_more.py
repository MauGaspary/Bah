from starlette.requests import Request

from app.config.model import get_embedding_model


def test_model_mock_lista_quando_testing_true(monkeypatch):

    monkeypatch.setenv("TESTING", "true")

    req = Request(scope={"type": "http"})
    m = get_embedding_model(req)

    assert hasattr(m, "encode")

    out_single = m.encode("abc")
    assert isinstance(out_single, list) and len(out_single) > 0
    assert all(isinstance(x, float) for x in out_single)

    out_batch = m.encode(["a", "b", "c"])
    assert isinstance(out_batch, list) and len(out_batch) == 3
    assert all(isinstance(v, list) for v in out_batch)


def test_model_mock_string_quando_testing_true(monkeypatch):

    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("EMBEDDING_MOCK_RETURNS", "string")

    req = Request(scope={"type": "http"})
    m = get_embedding_model(req)

    assert hasattr(m, "encode")
    out = m.encode("abc")
    assert isinstance(out, list) and len(out) > 0
