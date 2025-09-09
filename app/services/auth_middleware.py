from functools import wraps

from fastapi import HTTPException, Request
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidIssuerError,
    InvalidSignatureError,
)

from app.services.jwt_service import verify


def jwt_required(func):

    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid header")

        token = auth.split(" ", 1)[1] if len(auth.split(" ", 1)) > 1 else ""
        if not token.strip():
            raise HTTPException(status_code=401, detail="Missing token")

        try:
            claims = verify(token)

            request.state.user = {
                "userId": claims["sub"],
                "email": claims["email"],
                "iat": claims["iat"],
            }
        except (
            ExpiredSignatureError,
            InvalidIssuerError,
            InvalidSignatureError,
            DecodeError,
        ) as exc:
            raise HTTPException(status_code=401, detail="Invalid token") from exc

        return await func(request, *args, **kwargs)

    return wrapper
