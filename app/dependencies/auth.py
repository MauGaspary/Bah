from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()


def get_current_user(
    request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """Extrai o ID do usuário do token JWT através do middleware"""
    return request.state.user["userId"]
