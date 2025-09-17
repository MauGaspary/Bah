from fastapi import Request
from fastapi.responses import JSONResponse
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidIssuerError,
    InvalidSignatureError,
)
from starlette.middleware.base import BaseHTTPMiddleware

from app.services.jwt_service import verify


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/admin/") and not request.url.path.startswith(
            "/demo/"
        ):
            auth = request.headers.get("Authorization")

            if not auth or not auth.startswith("Bearer "):
                return JSONResponse(
                    status_code=401, content={"detail": "Authorization header required"}
                )

            parts = auth.split(" ", 1)
            token = parts[1] if len(parts) == 2 else ""

            if not token.strip():
                return JSONResponse(
                    status_code=401, content={"detail": "Token required"}
                )

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
            ):
                return JSONResponse(
                    status_code=401, content={"detail": "Invalid token"}
                )

        response = await call_next(request)
        return response
