import importlib


def test_settings_reload_production(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("JWT_SECRET", "secret-prod")
    monkeypatch.setenv("JWT_TTL", "3600")
    monkeypatch.setenv("JWT_ISS", "your_issuer")
    monkeypatch.setenv("ALGORITHM", "HS256")

    import app.config.settings as settings

    importlib.reload(settings)

    assert settings.JWT_SECRET == "secret-prod"
    assert isinstance(settings.JWT_TTL, int)
    assert settings.JWT_ISS == "your_issuer"
    assert settings.ALGORITHM == "HS256"


def test_settings_reload_ambiente_desconhecido_usa_fallback(monkeypatch):
    monkeypatch.setenv("APP_ENV", "x-unknown-env")
    monkeypatch.setenv("JWT_SECRET", "secret-unk")
    monkeypatch.setenv("JWT_TTL", "1800")
    monkeypatch.setenv("JWT_ISS", "your_issuer")
    monkeypatch.setenv("ALGORITHM", "HS256")

    import app.config.settings as settings

    importlib.reload(settings)

    assert settings.JWT_SECRET == "secret-unk"
    assert isinstance(settings.JWT_TTL, int)
