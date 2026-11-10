from tests.helpers import request_auth


def test_startup_executes_with_lifespan(client, auth_token):
    """Teste do startup do lifespan"""
    response = request_auth(client, "GET", "/admin/iniciativas", token=auth_token)
    assert response.status_code == 200
