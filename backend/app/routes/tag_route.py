from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.tag_controller import TagController
from app.dependencies.auth import get_current_user
from app.schemas.tag_schema import TagCreate, TagResponse, TagUpdate

router = APIRouter()


@router.get("/", response_model=List[TagResponse])
def listar_tags(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    controller = TagController(db)
    return controller.list_all()


@router.get("/{tag_id}", response_model=TagResponse)
def get_tag_by_id(
    tag_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    controller = TagController(db)
    return controller.get_by_id(tag_id)


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_data: TagCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    controller = TagController(db)
    return controller.create(tag_data)


@router.patch("/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_id: str,
    tag_data: TagUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    controller = TagController(db)
    return controller.update(tag_id, tag_data)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    controller = TagController(db)
    controller.delete(tag_id)
