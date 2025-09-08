import io
from contextlib import redirect_stdout

from fastapi.testclient import TestClient

from app.config.settings import Settings
from app.main import create_app
from tests.helpers import request


def test_startup_executes_with_lifespan(client):
    """Teste do startup do lifespan"""
    response = request(client, "GET", "/admin/")
    assert response.status_code == 200


def test_logging_setup_message():
    """Testa que a mensagem de configuração de logging é exibida"""
    settings = Settings(
        enable_logging_setup=True,
        log_level="DEBUG",
        testing=False,
        enable_database=False,
        database_url="sqlite:///:memory:",
    )

    captured_output = io.StringIO()

    with redirect_stdout(captured_output):
        app = create_app(settings)
        with TestClient(app) as client:
            request(client, "GET", "/")

    output = captured_output.getvalue()
    assert "Configurando logging - Level: DEBUG" in output
