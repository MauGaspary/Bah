import time

import jwt
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidIssuerError,
    InvalidSignatureError,
)

import app.config.settings as settings


def sign(sub: str, email: str, name: str) -> str:

    iat = int(time.time())
    exp = iat + settings.JWT_TTL
    payload = {
        "sub": sub,
    "email": email,
    "name": name,
        "iat": iat,
        "exp": exp,
        "iss": settings.JWT_ISS,
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    return token


def verify(token: str) -> dict:

    try:
        claims = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            issuer=settings.JWT_ISS,
        )
        return claims

    except ExpiredSignatureError:
        raise
    except InvalidSignatureError:
        raise
    except InvalidIssuerError:
        raise
    except DecodeError:
        raise
