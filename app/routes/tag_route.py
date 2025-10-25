from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.tag_controller import TagController
from app.schemas.tag_schema import TagResponse

router = APIRouter()


@router.get("/", response_model=List[TagResponse])
def listar_tags(db: Session = Depends(get_db)):
    controller = TagController(db)
    return controller.list_all()
