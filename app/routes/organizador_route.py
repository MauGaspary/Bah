from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.organizador_controller import OrganizadorController
from app.dependencies.auth import get_current_user
from app.schemas.organizador_schema import (
    OrganizadorCreate,
    OrganizadorResponse,
    OrganizadorUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[OrganizadorResponse])
def listar_organizadores(db: Session = Depends(get_db)):
    controller = OrganizadorController(db)
    return controller.list_all()


@router.get("/{organizador_id}", response_model=OrganizadorResponse)
def get_organizador_by_id(organizador_id: str, db: Session = Depends(get_db)):
    controller = OrganizadorController(db)
    return controller.get_by_id(organizador_id)


@router.post(
    "/", response_model=OrganizadorResponse, status_code=status.HTTP_201_CREATED
)
def create_organizador(
    organizador_data: OrganizadorCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    controller = OrganizadorController(db)
    return controller.create(organizador_data)


@router.patch("/{organizador_id}", response_model=OrganizadorResponse)
def update_organizador(
    organizador_id: str,
    organizador_data: OrganizadorUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    controller = OrganizadorController(db)
    return controller.update(organizador_id, organizador_data)


@router.delete("/{organizador_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organizador(
    organizador_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    controller = OrganizadorController(db)
    controller.delete(organizador_id)
