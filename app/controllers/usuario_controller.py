from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.usuario_schema import *
from app.services.usuario_service import UsuarioService


class UsuarioController:
    def __init__(self, db: Session):
        self.service = UsuarioService(db)

    def delete_usuario(self, usuario_id: str) -> bool:
        try:
            return self.service.delete_usuario(usuario_id)
        except ValueError as e:
            raise HTTPException(404, str(e)) from e
        except RuntimeError as e:
            raise HTTPException(500, str(e)) from e

    def get_usuario_by_id(self, usuario_id: str) -> UsuarioResponse:
        try:
            return self.service.get_usuario_by_id(usuario_id)
        except ValueError as e:
            raise HTTPException(404, str(e)) from e
