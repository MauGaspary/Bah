from sqlalchemy.orm import Session

from app.models.usuario_model import Usuario
from app.schemas.user_schema import UserResponse, UserUpdate


class UserController:
    def __init__(self, db: Session):
        self.db = db

    def update_user(self, user_id: str, user_data: UserUpdate):
        user = self.db.query(Usuario).filter(Usuario.id == user_id).first()
        if not user:
            return None

        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user
