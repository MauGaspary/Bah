import pytest

from app.config.settings import (
    Settings,
    get_development_settings,
    get_production_settings,
    get_settings,
    get_test_settings,
)


class TestSettings:
    """Testes para as configurações da aplicação."""

    def test_settings_dataclass_creation(self):
        """Testa criação básica da dataclass Settings."""
        settings = Settings()

        # Verificar valores padrão
        assert settings.database_url is None
        assert settings.database_echo is False
        assert settings.log_level == "INFO"
        assert settings.debug is False
        assert settings.testing is False
        assert settings.enable_database is True
        assert settings.enable_logging_setup is True

    def test_settings_with_custom_values(self):
        """Testa criação de Settings com valores customizados."""
        settings = Settings(
            database_url="custom://localhost",
            debug=True,
            log_level="DEBUG",
        )

        assert settings.database_url == "custom://localhost"
        assert settings.debug is True
        assert settings.log_level == "DEBUG"

    def test_get_development_settings(self):
        """Testa configurações de desenvolvimento."""
        settings = get_development_settings()

        # Validar configurações específicas de desenvolvimento
        assert settings.database_url == "sqlite:///bah.db"
        assert settings.database_echo is True
        assert settings.log_level == "DEBUG"
        assert settings.debug is True
        assert settings.testing is False
        assert settings.enable_database is True
        assert settings.enable_logging_setup is True

    def test_get_test_settings(self):
        """Testa configurações de teste."""
        settings = get_test_settings()

        # Validar configurações específicas de teste
        assert (
            "postgresql://" in settings.database_url
            or settings.database_url == "sqlite:///:memory:"
        )
        assert settings.database_echo is False
        assert settings.log_level == "WARNING"
        assert settings.debug is False
        assert settings.testing is True
        assert settings.enable_database is True
        assert settings.enable_logging_setup is False  # Desabilitado em testes

    def test_get_production_settings(self):
        """Testa configurações de produção."""
        settings = get_production_settings()

        # Validar configurações específicas de produção
        assert "postgresql://" in settings.database_url
        assert settings.database_echo is False
        assert settings.log_level == "INFO"
        assert settings.debug is False
        assert settings.testing is False
        assert settings.enable_database is True
        assert settings.enable_logging_setup is True

    def test_get_settings_returns_development_by_default(self):
        """Testa que get_settings() retorna configurações de desenvolvimento por padrão."""
        settings = get_settings()
        dev_settings = get_development_settings()

        # Deve retornar as mesmas configurações de desenvolvimento
        assert settings.database_url == dev_settings.database_url
        assert settings.debug == dev_settings.debug
        assert settings.testing == dev_settings.testing

    def test_all_environments_have_consistent_structure(self):
        """Testa que todas as configurações de ambiente têm a mesma estrutura."""
        dev_settings = get_development_settings()
        test_settings = get_test_settings()
        prod_settings = get_production_settings()

        # Todos devem ter os mesmos atributos
        for settings in [dev_settings, test_settings, prod_settings]:
            assert hasattr(settings, "database_url")
            assert hasattr(settings, "database_echo")
            assert hasattr(settings, "log_level")
            assert hasattr(settings, "debug")
            assert hasattr(settings, "testing")
            assert hasattr(settings, "enable_database")
            assert hasattr(settings, "enable_logging_setup")

            # Tipos devem estar corretos
            assert isinstance(settings.debug, bool)
            assert isinstance(settings.testing, bool)
            assert isinstance(settings.enable_database, bool)
            assert isinstance(settings.enable_logging_setup, bool)
            assert isinstance(settings.log_level, str)
