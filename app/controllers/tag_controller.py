from typing import List

from sqlalchemy.orm import Session

from app.schemas.tag_schema import TagResponse
from app.services.tag_service import TagService


class TagController:

    def __init__(self, db: Session):
        self.service = TagService(db)

    def list_all(self) -> List[TagResponse]:
        return self.service.list_all()
