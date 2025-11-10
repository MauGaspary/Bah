from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.usuario_controller import UsuarioController
from app.dependencies.auth import get_current_user
from app.schemas.usuario_schema import UserCreate, UserResponse, UsersResponse

security = HTTPBearer()

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    controller = UsuarioController(db)
    return controller.create_user(user)


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(
    usuario_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """
    Deleta um usuário pelo ID (requer autenticação).
    - Idempotente: múltiplas chamadas retornam 204
    - Retorna 404 se o usuário não existir
    """
    controller = UsuarioController(db)
    controller.delete_usuario(usuario_id)


@router.get("/{usuario_id}", response_model=UserResponse)
def get_user_by_id(
    usuario_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    controller = UsuarioController(db)
    return controller.get_usuario_by_id(usuario_id)


@router.get("/", response_model=UsersResponse)
def list_users(
    q: Optional[str] = Query(None, description="Search query (nome or email)"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    controller = UsuarioController(db)
    return controller.list_users(page=page, size=size, q=q)
