from fastapi import HTTPException
from app.utils.passwordHasher import PasswordHasher
from app.services.jwt_service import sign
from app.config.settings import JWT_TTL

class AuthController:
    def __init__(self):
        #banco

        self.hasher = PasswordHasher()
        pass

    def login(self, email: str, password: str):
        #buscar user no banco com email

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not self.hasher.verify(password user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = sign(sub=str(user.id), email=user.email)

        return {
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": 1800 #diferente do JWT_TTL
        }