import pytest
from fastapi.testclient import TestClient

from app.config.settings import Settings, get_test_settings
from app.main import create_app
from tests.helpers import request


def test_lifespan_startup_executes():
    """
    Teste que verifica se o lifespan startup/shutdown executa corretamente.

    Valida que:
    - create_app() funciona com settings
    - TestClient dispara o lifespan startup
    - Settings são aplicadas na aplicação
    - Shutdown executa automaticamente
    """
    # Criar configurações específicas para teste
    settings = get_test_settings()

    # Criar uma nova instância da aplicação
    app = create_app(settings)

    # TestClient dispara o lifespan startup automaticamente
    with TestClient(app) as client:
        # Verificar se a aplicação está respondendo
        # Nota: O endpoint "/" retorna HTML (docs), vamos testar outro endpoint
        response = request(client, "GET", "/admin/")

        # Validar resposta do endpoint admin
        assert response.status_code == 200

        # Verificar se as settings foram aplicadas corretamente
        assert app.state.settings.testing is True
        assert app.state.settings.enable_logging_setup is False

    # Shutdown executa automaticamente ao sair do contexto


def test_different_settings():
    """
    Teste que valida o comportamento da aplicação com configurações customizadas.

    Verifica se:
    - Settings customizadas são aplicadas
    - Aplicação funciona com diferentes configurações
    - Lifespan respeita flags de habilitação/desabilitação
    """
    # Criar configurações customizadas
    custom_settings = Settings(
        database_url="sqlite:///:memory:",
        testing=True,
        debug=False,
        enable_database=False,
        enable_logging_setup=False,
    )

    # Criar aplicação com configurações customizadas
    app = create_app(custom_settings)

    # Testar funcionamento com configurações diferentes
    with TestClient(app) as client:
        response = request(client, "GET", "/")
        assert response.status_code == 200

        # Validar se configurações foram aplicadas
        assert app.state.settings.enable_database is False
        assert app.state.settings.testing is True
