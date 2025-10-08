from typing import Optional

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.usuario_controller import UsuarioController
from app.schemas.usuario_schema import UsuarioDelete, UsuarioResponse

security = HTTPBearer()

router = APIRouter()


@router.post(
    "/users", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED
)
def delete_usuario(
    usuario_id: str,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> bool:
    """Deleta um usuário."""
    controller = db
    return controller.delete_usuario(usuario_id)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def get_usuario_by_id(
    usuario_id: str,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Busca um usuário pelo ID."""
    controller = UsuarioController(db)
    return controller.get_usuario_by_id(str(usuario_id))
