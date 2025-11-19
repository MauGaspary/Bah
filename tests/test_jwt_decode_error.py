import jwt
import pytest
from jwt.exceptions import DecodeError

from app.services import jwt_service


def test_verify_token_malformado_dispara_decode_error():
    with pytest.raises(DecodeError):
        jwt_service.verify("isto-nao-e-um-jwt")


def test_verify_token_invalida_issuer(monkeypatch):
    monkeypatch.setattr(jwt_service.settings, "JWT_SECRET", "secret")
    monkeypatch.setattr(jwt_service.settings, "ALGORITHM", "HS256")
    monkeypatch.setattr(jwt_service.settings, "JWT_ISS", "issuer")
    import time

    token = jwt.encode(
        {
            "sub": "user",
            "email": "user@example.com",
            "iss": "outro",
            "iat": int(time.time()),
            "exp": int(time.time()) + 60,
        },
        "secret",
        algorithm="HS256",
    )

    from jwt.exceptions import InvalidIssuerError

    with pytest.raises(InvalidIssuerError):
        jwt_service.verify(token)
