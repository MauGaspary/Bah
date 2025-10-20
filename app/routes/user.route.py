from turtle import st

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.user_controller import UserController
from app.dependencies.auth import get_current_user
from app.schemas.user_schema import UserResponse, UserUpdate

router = APIRouter()


@router.put(
    "/usuarios/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_user(
    user_id: str,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):

    controller = UserController(db)
    update_user = controller.update_user(user_id, user_update)
    if not update_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )
    return update_user
