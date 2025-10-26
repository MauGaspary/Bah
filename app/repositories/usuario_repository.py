from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UserCreate
from app.utils.password_hasher import PasswordHasher


class UsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> Optional[Usuario]:
        stmt = select(Usuario).where(func.lower(Usuario.email) == func.lower(email))
        return self.session.execute(stmt).scalars().first()

    def email_exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def create(self, user_data: UserCreate) -> Usuario:
        email_norm = user_data.email.strip()
        hasher = PasswordHasher()
        usuario = Usuario(
            email=email_norm,
            senha_hash=hasher.hash(user_data.password),
            nome=user_data.nome,
            sobrenome=user_data.sobrenome,
        )
        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)

        return usuario

    def get_by_id(self, user_id: str) -> Optional[Usuario]:
        stmt = select(Usuario).where(Usuario.id == user_id)
        return self.session.execute(stmt).scalars().first()

    def delete(self, user_id: str) -> bool:
        try:
            deleted = self.session.query(Usuario).filter(Usuario.id == user_id).delete()
            if deleted:
                self.session.commit()
                return True
            return False
        except Exception:
            self.session.rollback()
            raise
