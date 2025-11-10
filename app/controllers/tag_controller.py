from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.tag_schema import TagCreate, TagResponse, TagUpdate
from app.services.tag_service import TagService
from app.utils.exceptions import ResourceNotFoundException


class TagController:

    def __init__(self, db: Session):
        self.service = TagService(db)

    def list_all(self) -> List[TagResponse]:
        return self.service.list_all()

    def get_by_id(self, tag_id: str) -> TagResponse:
        try:
            return self.service.get_by_id(tag_id)
        except ResourceNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e

    def create(self, tag_data: TagCreate) -> TagResponse:
        try:
            return self.service.create(tag_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    def update(self, tag_id: str, tag_data: TagUpdate) -> TagResponse:
        try:
            return self.service.update(tag_id, tag_data)
        except ResourceNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    def delete(self, tag_id: str) -> None:
        try:
            self.service.delete(tag_id)
        except ResourceNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
