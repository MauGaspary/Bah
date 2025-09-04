from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base


class IniciativaTag(Base):
    __tablename__ = "iniciativa_tag"

    iniciativa_id = Column(UUID(as_uuid=True), ForeignKey("iniciativas.id"), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True)

    __table_args__ = (UniqueConstraint("iniciativa_id", "tag_id", name="uq_iniciativa_tag"),)
