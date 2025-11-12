from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.usuario_schema import UserCreate, UserResponse
from app.services.usuario_service import UsuarioService


class UsuarioController:
    def __init__(self, db: Session):
        self.service = UsuarioService(db)

    def create_user(self, user: UserCreate) -> UserResponse:
        return self.service.create_user(user)

    def delete_usuario(self, usuario_id: str) -> bool:
        try:
            return self.service.delete_usuario(usuario_id)
        except ValueError as e:
            raise HTTPException(404, str(e)) from e
        except RuntimeError as e:
            raise HTTPException(500, str(e)) from e

    def get_usuario_by_id(self, usuario_id: str) -> UserResponse:
        try:
            return self.service.get_usuario_by_id(usuario_id)
        except ValueError as e:
            raise HTTPException(404, str(e)) from e

    def list_users(
        self, page: int = 1, size: int = 10, q: Optional[str] = None
    ) -> dict:
        try:
            items, total = self.service.list_users(page=page, size=size, q=q)
            return {"items": items, "total": total}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
