import importlib
import os


def _clear_cache_if_any(func):
    try:
        func.cache_clear()
    except AttributeError:
        pass


def test_settings_env_invalido_usa_fallback(monkeypatch):
    monkeypatch.setenv("APP_ENV", "invalid_env_value")
    import app.config.settings as settings_mod

    importlib.reload(settings_mod)
    _clear_cache_if_any(settings_mod.get_settings)
    s = settings_mod.get_settings()

    assert s is not None


def test_settings_env_test(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    import app.config.settings as settings_mod

    importlib.reload(settings_mod)
    settings = settings_mod.get_settings()
    assert settings.testing is True
    assert settings.jwt_secret == "fake-test-secret-key"


def test_settings_env_production(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    import app.config.settings as settings_mod

    importlib.reload(settings_mod)
    settings = settings_mod.get_settings()
    assert settings.testing is False
    assert settings.log_level == "INFO"
