USUARIOS_PATH = "/admin/usuarios"


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_usuario_route_metodo_nao_permitido(client, auth_token):

    resp = client.get(USUARIOS_PATH, headers=_auth_headers(auth_token))
    assert resp.status_code in (404, 405)


def test_usuario_route_content_type_incorreto(client, auth_token):

    headers = _auth_headers(auth_token)
    headers["Content-Type"] = "text/plain"
    resp = client.post(USUARIOS_PATH, headers=headers, content="nome=PH&email=x@y.z")
    assert resp.status_code in (400, 415, 422)


def test_usuario_controller_payload_vazio(client, auth_token):

    resp = client.post(USUARIOS_PATH, headers=_auth_headers(auth_token), json={})
    assert resp.status_code in (400, 422)


def test_usuario_route_delete_invoca_controller(monkeypatch):
    import app.routes.usuario_route as route_mod

    called = {}

    class FakeController:
        def __init__(self, db): ...

        def delete_usuario(self, usuario_id):
            called["id"] = usuario_id
            return True

    monkeypatch.setattr(route_mod, "UsuarioController", FakeController)
    assert route_mod.delete_usuario("123", db=None, current_user="token") is None
    assert called["id"] == "123"


def test_usuario_route_get_invoca_controller(monkeypatch):
    import app.routes.usuario_route as route_mod

    class FakeController:
        def __init__(self, db): ...

        def get_usuario_by_id(self, usuario_id):
            return {"id": usuario_id}

    monkeypatch.setattr(route_mod, "UsuarioController", FakeController)
    result = route_mod.get_user_by_id("xyz", db=None, current_user="token")
    assert result["id"] == "xyz"
