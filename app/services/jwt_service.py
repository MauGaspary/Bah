import jwt
import time
import app.config.settings as settings

from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
    InvalidIssuerError,
    DecodeError,
)


def sign(sub: str, email: str) -> str:

    iat = int(time.time())
    exp = iat + settings.JWT_TTL
    payload = {
        "sub":sub,
        "email":email,
        "iat":iat,
        "exp":exp,
        "iss":settings.JWT_ISS,
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
        raise #token expirou
    except InvalidSignatureError:
        raise #assinatura invalida
    except InvalidIssuerError:
        raise #emissor invalido
    except DecodeError:
        raise #formato invalido do token