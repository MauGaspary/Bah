from fastapi import HTTPException
from app.utils.passwordHasher import PasswordHasher
from app.services.jwt_service import sign
from app.config.settings import JWT_TTL

from app.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session

class AuthController:
    def __init__(self, db_session: Session):
        self.hasher = PasswordHasher()
        self.user_repo = UserRepository(db_session)

    def login(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not self.hasher.verify(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials password")
        
        token = sign(sub=str(user.id), email=user.email)

        return {
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": JWT_TTL #diferente do JWT_TTL
        }