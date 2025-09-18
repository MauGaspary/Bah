import pytest

from app.services.auth_service import AuthService
from app.utils.exceptions import InvalidCredentialsException


def test_authenticate_success(db_session, test_user):
    auth_service = AuthService(db_session)

    result = auth_service.authenticate("teste@gmail.com", "senha123")

    assert "access_token" in result
    assert result["token_type"] == "Bearer"
    assert "expires_in" in result


def test_authenticate_invalid_email(db_session):
    auth_service = AuthService(db_session)

    with pytest.raises(InvalidCredentialsException):
        auth_service.authenticate("invalid@email.com", "senha123")


def test_authenticate_invalid_password(db_session, test_user):
    auth_service = AuthService(db_session)

    with pytest.raises(InvalidCredentialsException):
        auth_service.authenticate("teste@gmail.com", "wrong_password")
