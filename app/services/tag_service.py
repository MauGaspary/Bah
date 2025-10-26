from typing import List

from sqlalchemy.orm import Session

from app.repositories.tag_repository import TagRepository
from app.schemas.tag_schema import TagResponse


class TagService:

    def __init__(self, db: Session):
        self.repository = TagRepository(db)

    def list_all(self) -> List[TagResponse]:
        tags = self.repository.list_all()
        return [TagResponse.model_validate(tag) for tag in tags]
