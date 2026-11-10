import uuid

from sqlalchemy import Column, String

from app.models.base import Base


class Organizador(Base):
    __tablename__ = "organizadores"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    nome = Column(String, nullable=False, unique=True, index=True)
