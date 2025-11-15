import time

import jwt
import pytest
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidIssuerError,
    InvalidSignatureError,
)

import app.config.settings as settings
from app.config.settings import ALGORITHM, JWT_ISS, JWT_SECRET
from app.services.jwt_service import sign, verify


def test_sign_verify_correct():
    token = sign("12345", "admin@teste.com", "Admin")
    claims = verify(token)
    assert claims["sub"] == "12345"
    assert claims["email"] == "admin@teste.com"
    assert claims["name"] == "Admin"
    assert claims["iss"] == JWT_ISS


def test_payload_invalid():
    token = sign("12345", "admin@teste.com", "Admin")
    token_invalido = token + "invalidandoToken"
    with pytest.raises((InvalidSignatureError, DecodeError)):
        verify(token_invalido)


def test_wrong_secret():
    token = sign("12345", "admin@teste.com", "Admin")
    with pytest.raises(InvalidSignatureError):
        jwt.decode(token, "segredoErrado", algorithms=[ALGORITHM])


def test_expired_token():
    ttl_original = settings.JWT_TTL
    settings.JWT_TTL = 1
    token = sign("12345", "admin@teste.com", "Admin")
    time.sleep(2)
    with pytest.raises(ExpiredSignatureError):
        verify(token)
    settings.JWT_TTL = ttl_original


def test_invalid_iss():
    token = sign("12345", "admin@teste.com")
    with pytest.raises(InvalidIssuerError):
        jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM], issuer="issuer-invalido")
