from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.organizador_controller import OrganizadorController
from app.schemas.organizador_schema import OrganizadorResponse

router = APIRouter()


@router.get("/", response_model=List[OrganizadorResponse])
def listar_organizadores(db: Session = Depends(get_db)):
    controller = OrganizadorController(db)
    return controller.list_all()


@router.get("/{organizador_id}", response_model=OrganizadorResponse)
def get_organizador_by_id(organizador_id: str, db: Session = Depends(get_db)):
    controller = OrganizadorController(db)
    return controller.get_by_id(organizador_id)
