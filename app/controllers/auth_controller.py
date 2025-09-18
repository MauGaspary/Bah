from sqlalchemy.orm import Session

from app.services.auth_service import AuthService


class AuthController:
    def __init__(self, db_session: Session):
        self.auth_service = AuthService(db_session)

    def login(self, email: str, password: str):
        return self.auth_service.authenticate(email, password)
