from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.auth_service import AuthService
from app.utils.exceptions import InvalidCredentialsException


class AuthController:
    def __init__(self, db_session: Session):
        self.auth_service = AuthService(db_session)

    def login(self, email: str, password: str):
        try:
            return self.auth_service.authenticate(email, password)
        except InvalidCredentialsException as e:
            raise HTTPException(401, str(e)) from e
