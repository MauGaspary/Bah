from typing import List

from sqlalchemy.orm import Session

from app.models.tag_model import Tag


class TagRepository:

    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> List[Tag]:
        return self.session.query(Tag).all()
