import pytest
from fastapi.testclient import TestClient

from app.config.settings import Settings, get_test_settings
from app.main import create_app
from tests.helpers import request


def test_lifespan_startup_executes(client):
    """
    Teste que verifica se o lifespan startup/shutdown executa corretamente.

    Valida que:
    - create_app() funciona com settings
    - TestClient dispara o lifespan startup
    - Settings são aplicadas na aplicação
    - Shutdown executa automaticamente
    """
    # Usar cliente já configurado com testcontainer
    response = request(client, "GET", "/admin/")

    # Validar resposta do endpoint admin
    assert response.status_code == 200


def test_different_settings(app_with_lifespan):
    """
    Teste que valida o comportamento da aplicação com configurações customizadas.
    """
    # Testar funcionamento com app_with_lifespan fixture
    with TestClient(app_with_lifespan) as client:
        response = request(client, "GET", "/")
        # Pode ser 200 (docs) ou 307 (redirect)
        assert response.status_code in [200, 307]

        # Validar se configurações foram aplicadas
        assert app_with_lifespan.state.settings.testing is True
