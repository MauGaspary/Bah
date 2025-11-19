import time

import jwt
import pytest
from jwt.exceptions import ImmatureSignatureError

import app.config.settings as settings
from app.services.jwt_service import verify


def test_jwt_rejeita_token_com_nbf_no_futuro():
    now = int(time.time())
    payload = {
        "sub": "u123",
        "email": "u@example.com",
        "iat": now,
        "exp": now + settings.JWT_TTL,
        "iss": settings.JWT_ISS,
        "nbf": now + 600,
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    with pytest.raises(ImmatureSignatureError):
        verify(token)
