import uuid

from sqlalchemy import Column, String, Text

from app.models.base import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    nome = Column(String, nullable=False, unique=True, index=True)
    descricao = Column(Text)
