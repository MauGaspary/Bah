from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UserCreate, UserResponse
from app.utils.exceptions import EmailAlreadyExistsException
from app.utils.helpers import validate_email


class UsuarioService:
    def __init__(self, db: Session):
        self.repository = UsuarioRepository(db)

    def create_user(self, user_data: UserCreate) -> UserResponse:
        if not validate_email(user_data.email):
            raise ValueError("Formato de email inválido")

        if self.repository.get_by_email(user_data.email):
            raise EmailAlreadyExistsException("Email já está em uso")

        try:
            user = self.repository.create(user_data)
            return UserResponse.model_validate(user)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erro interno do servidor: {str(e)}"
            ) from e

    def delete_usuario(self, usuario_id: str) -> bool:
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario não encontrado")

        success = self.repository.delete(usuario_id)
        if not success:
            raise RuntimeError("Erro ao deletar usuário")
        return True

    def get_usuario_by_id(self, usuario_id: str) -> UserResponse:
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario não encontrado")
        return UserResponse.model_validate(usuario)

    def list_users(
        self, page: int = 1, size: int = 10, q: Optional[str] = None
    ) -> tuple[list[UserResponse], int]:
        skip = max(0, (page - 1) * size)
        try:
            items, total = self.repository.list(skip=skip, limit=size, q=q)
            users = [UserResponse.model_validate(u) for u in items]
            return users, total
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erro interno do servidor: {str(e)}"
            ) from e
