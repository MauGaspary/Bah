from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate
from app.utils.password_hasher import PasswordHasher


class UsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> Optional[Usuario]:
        stmt = select(Usuario).where(func.lower(Usuario.email) == func.lower(email))
        return self.session.execute(stmt).scalars().first()

    def email_exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def create1(self, user_data: UsuarioCreate) -> Usuario:
        email_norm = user_data.email.strip()
        hasher = PasswordHasher()
        usuario = Usuario (
            email=email_norm,
            senha_hash=hasher.hash(user_data.password),
            nome=user_data.nome,
            sobrenome=user_data.sobrenome,
        ) 
        self.session.add(usuario)
        self.session.flush()
        self.session.refresh(usuario)
        return usuario

    def create2(self, email: str, password: str, nome: str, sobrenome: str) -> Usuario:
        email_norm = email.strip()
        hasher = PasswordHasher()
        usuario = Usuario(
            email=email_norm,
            senha_hash=hasher.hash(password),
            nome=nome,
            sobrenome=sobrenome,
        )
        self.session.add(usuario)
        self.session.flush()
        return usuario
