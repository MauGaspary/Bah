"""
Configurações da aplicação BAH.

Este arquivo define as configurações que podem ser diferentes
entre ambientes (dev, test, prod).
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    """Configurações da aplicação."""

    database_url: Optional[str] = None
    database_echo: bool = False

    log_level: str = "INFO"

    debug: bool = False
    testing: bool = False

    enable_database: bool = True
    enable_logging_setup: bool = True

    jwt_secret: str = "your-secret-key"
    jwt_ttl_seconds: int = 3600


def get_development_settings() -> Settings:
    """Configurações para desenvolvimento."""
    return Settings(
        database_url="postgresql://bah_user:bah_password@localhost:5432/bah_db",
        database_echo=True,
        log_level="DEBUG",
        debug=True,
        testing=False,
    )


def get_test_settings() -> Settings:
    """Configurações para testes."""
    return Settings(
        database_url="postgresql://bah_user:bah_password@localhost:5432/bah_db",
        database_echo=False,
        log_level="WARNING",
        debug=False,
        testing=True,
        enable_logging_setup=False,
        jwt_secret="fake-test-secret-key",
        jwt_ttl_seconds=60,
    )


def get_production_settings() -> Settings:
    """Configurações para produção."""
    return Settings(
        database_url="postgresql://user:pass@localhost/bah_db",
        database_echo=False,
        log_level="INFO",
        debug=False,
        testing=False,
    )


def get_settings() -> Settings:
    """Retorna as configurações baseadas no ambiente."""
    import os

    env = os.getenv("APP_ENV", "development").lower()

    if env == "test":
        return get_test_settings()
    if env == "production":
        return get_production_settings()
    return get_development_settings()
