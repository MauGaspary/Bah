from sqlalchemy import Column, ForeignKey, String, Index
from app.config.database import Base


class IniciativaTag(Base):
    __tablename__ = "iniciativa_tag"

    iniciativa_id = Column(String, ForeignKey("iniciativas.id"), primary_key=True)
    tag_id = Column(String, ForeignKey("tags.id"), primary_key=True)

    __table_args__ = (
        Index("idx_iniciativa_tag_unique", "iniciativa_id", "tag_id", unique=True),
    )
