from fastapi.testclient import TestClient

from app.main import app


def test_generic_exception_handler_captura_erro():
    def boom():
        raise RuntimeError("boom")

    path = "/__boom500_ok"
    app.add_api_route(path, boom, methods=["GET"])

    client = TestClient(app, raise_server_exceptions=False)

    resp = client.get(path)
    assert resp.status_code == 500

    ct = resp.headers.get("content-type", "")
    if "application/json" in ct:
        body = resp.json()
        assert isinstance(body, dict)
        assert any(k in body for k in ("detail", "message"))
    else:

        assert resp.text.strip() != ""
