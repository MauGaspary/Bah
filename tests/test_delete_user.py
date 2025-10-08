import pytest

from app.services.usuario_service import UsuarioService


def test_delete_existing_user(db_session):
    service = UsuarioService(db_session)
    result = service.delete_usuario("1")
    assert result is True


def test_delete_nonexisting_user(db_session):
    service = UsuarioService(db_session)
    with pytest.raises(ValueError) as excinfo:
        service.delete_usuario("9999")
    assert "Usuario não encontrado" in str(excinfo.value)
