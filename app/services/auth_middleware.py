from fastapi import Request, HTTPException
from functools import wraps

from app.services.jwt_service import verify
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, InvalidIssuerError, DecodeError

def jwt_required(func):
    
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid header")
        
        try:
            token = auth.split(" ")[1]
            if not token:
                raise HTTPException(status_code=401, detail="Missing token")
        except IndexError:
            raise HTTPException(status_code=401, detail="Missing token")

        try:
            claims = verify(token)

            request.state.user = {
                "userId": claims["sub"],
                "email": claims["email"],
                "iat": claims["iat"],
            }
        except (ExpiredSignatureError, InvalidIssuerError, InvalidSignatureError, DecodeError):
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return await func(request, *args, **kwargs)
    
    return wrapper
