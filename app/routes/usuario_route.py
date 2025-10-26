from typing import Optional

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.usuario_controller import UsuarioController
from app.schemas.usuario_schema import UsuarioDelete, UsuarioResponse

security = HTTPBearer()

router = APIRouter()


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(
    usuario_id: str,
    db: Session = Depends(get_db),
):
    """
    Deleta um usuário pelo ID.
    - Idempotente: múltiplas chamadas retornam 204
    - Retorna 404 se o usuário não existir
    """
    controller = UsuarioController(db)
    controller.delete_usuario(usuario_id)
