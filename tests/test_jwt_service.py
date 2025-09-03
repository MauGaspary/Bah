import time
import pytest
import jwt
import app.config.settings as settings


from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidIssuerError,
    InvalidSignatureError,
    DecodeError,
)

from app.services.jwt_service import sign, verify
from app.config.settings import JWT_SECRET, JWT_ISS, ALGORITHM






#feliz
def test_sign_verify_correct():
    token = sign("12345", "admin@teste.com")
    claims = verify(token)
    assert claims["sub"] == "12345"
    assert claims["email"] == "admin@teste.com"
    assert claims["iss"] == JWT_ISS

#mudar payload
def test_payload_invalid():
    token = sign("12345", "admin@teste.com")
    tokenInvalido = token + "invalidandoToken"
    with pytest.raises((InvalidSignatureError, DecodeError)):
        verify(tokenInvalido)

#secret errado
def test_wrong_secret():
    token = sign("12345", "admin@teste.com")
    with pytest.raises(InvalidSignatureError):
        jwt.decode(token, "segredoErrado", algorithms=[ALGORITHM])

#assinatura expirada
def test_expired_token():
    TTL_original = settings.JWT_TTL #Não tenho certeza se é a melhor pratica pra alterar o TTL, parece meio estranho
    settings.JWT_TTL = 1
    token = sign("12345", "admin@teste.com")
    time.sleep(2)
    with pytest.raises(ExpiredSignatureError):
        verify(token)
    settings.JWT_TTL = TTL_original

#iss diferente
def test_invalid_iss():
    token = sign("12345", "admin@teste.com")
    with pytest.raises(InvalidIssuerError):
        jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM], issuer="issuer-invalido")





