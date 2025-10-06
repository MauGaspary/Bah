from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import UserService


class UserController:
    def __init__(self, db: Session):
        self.service = UserService(db)

    def create_user(self, user: UserCreate) -> UserResponse:
        return self.service.create_user(user)
