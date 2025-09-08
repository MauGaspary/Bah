"""Settings específicas para testes de integração"""

from .settings import Settings


def get_integration_test_settings(database_url: str) -> Settings:
    """Configurações para testes de integração com PostgreSQL"""
    return Settings(
        database_url=database_url,
        database_echo=False,
        log_level="WARNING",
        debug=False,
        testing=True,
        enable_logging_setup=False,
        jwt_secret="fake-test-secret-key",
        jwt_ttl_seconds=60,
    )
