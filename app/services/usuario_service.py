from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import *


class UsuarioService:
    def __init__(self, db: Session):
        self.repository = UsuarioRepository(db)

    def delete_usuario(self, usuario_id: str) -> bool:
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario não encontrado")

        success = self.repository.delete(usuario_id)
        if not success:
            raise RuntimeError("Erro ao deletar usuário")
        return True

    def get_usuario_by_id(self, usuario_id: str) -> UsuarioResponse:
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario não encontrado")
        return UsuarioResponse.model_validate(usuario)
