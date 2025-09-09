from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.usuario_model import Usuario
from app.utils.password_hasher import PasswordHasher


class UsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> Optional[Usuario]:
        stmt = select(Usuario).where(func.lower(Usuario.email) == func.lower(email))
        return self.session.execute(stmt).scalars().first()

    def create(self, email: str, password: str, nome: str, sobrenome: str) -> Usuario:
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
