from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserResponse
from app.utils.helpers import validate_email
from app.utils.exceptions import EmailAlreadyExistsException


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> UserResponse:
        if not validate_email(user_data.email):
            raise ValueError("Formato de email inválido")

        if self.repository.get_user_by_email(user_data.email):
            raise EmailAlreadyExistsException("Email já está em uso")

        try:
            user = self.repository.create(user_data)
            return UserResponse.model_validate(user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}") from e
