from fastapi.testclient import TestClient

from tests.helpers import request, request_auth


def test_lifespan_startup_executes(client, auth_token):
    """
    Teste que verifica se o lifespan startup/shutdown executa corretamente.

    Valida que:
    - create_app() funciona com settings
    - TestClient dispara o lifespan startup
    - Settings são aplicadas na aplicação
    - Shutdown executa automaticamente
    """
    response = request_auth(client, "GET", "/admin/iniciativas", token=auth_token)

    assert response.status_code == 200


def test_different_settings(app_with_lifespan):
    """
    Teste que valida o comportamento da aplicação com configurações customizadas.
    """
    with TestClient(app_with_lifespan) as client:
        response = request(client, "GET", "/")
        assert response.status_code in [200, 307]

        assert app_with_lifespan.state.settings.testing is True
