from sqlalchemy.orm import Session

from app.models.usuario_model import Usuario
from app.schemas.user_schema import UserResponse, UserUpdate, UserCreate
from app.services.user_service import UserService


class UserController:
    def __init__(self, db: Session):
        self.db = db
        self.service = UserService(db)

    def update_user(self, user_id: str, user_data: UserUpdate):
        user = self.db.query(Usuario).filter(Usuario.id == user_id).first()
        if not user:
            return None

        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def create_user(self, user: UserCreate) -> UserResponse:
        return self.service.create_user(user)
