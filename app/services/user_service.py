from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.user_schema import UserCreate, UserResponse
from app.utils.exceptions import EmailAlreadyExistsException
from app.utils.helpers import validate_email


class UserService:
    def __init__(self, db: Session):
        self.repository = UsuarioRepository(db)

    def create_user(self, user_data: UserCreate) -> UserResponse:
        if not validate_email(user_data.email):
            raise ValueError("Formato de email inválido")

        if self.repository.get_by_email(user_data.email):
            raise EmailAlreadyExistsException("Email já está em uso")

        try:
            user = self.repository.create1(user_data)
            return UserResponse.model_validate(user)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erro interno do servidor: {str(e)}"
            ) from e
