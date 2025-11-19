from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.tag_model import Tag


class TagRepository:

    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> List[Tag]:
        return self.session.query(Tag).all()

    def get_by_id(self, tag_id: str) -> Optional[Tag]:
        return self.session.query(Tag).filter(Tag.id == tag_id).first()

    def create(self, tag: Tag) -> Tag:
        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)
        return tag

    def update(self, tag: Tag) -> Tag:
        self.session.commit()
        self.session.refresh(tag)
        return tag

    def delete(self, tag: Tag) -> None:
        self.session.delete(tag)
        self.session.commit()
