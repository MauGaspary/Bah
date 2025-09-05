from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.utils.passwordHasher import PasswordHasher


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(func.lower(User.email) == func.lower(email))
        return self.session.execute(stmt).scalars().first()

    def create(self, email: str, password: str, name: Optional[str] = None) -> User:
        email_norm = email.strip()
        user = User(email=email_norm, password_hash=PasswordHasher.hash(password), name=name)
        self.session.add(user)
        self.session.flush()  # gera id
        return user
