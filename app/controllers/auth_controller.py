from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.config.settings import JWT_TTL
from app.repositories.usuario_repository import UsuarioRepository
from app.services.jwt_service import sign
from app.utils.password_hasher import PasswordHasher


class AuthController:
    def __init__(self, db_session: Session):
        self.hasher = PasswordHasher()
        self.usuario_repo = UsuarioRepository(db_session)

    def login(self, email: str, password: str):
        usuario = self.usuario_repo.get_by_email(email)

        if not usuario or not self.hasher.verify(password, usuario.senha_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = sign(sub=str(usuario.id), email=usuario.email)

        return {"access_token": token, "token_type": "Bearer", "expires_in": JWT_TTL}
