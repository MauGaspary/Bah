import os
import uuid

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.models.base import Base

MODEL_DIMENSION = int(os.getenv("MODEL_DIMENSIONS", "1024"))

try:
    from pgvector.sqlalchemy import Vector

    VectorType = Vector(MODEL_DIMENSION)
except ImportError:
    VectorType = Text


class DescricoesExtras(Base):
    __tablename__ = "descricoes_extras"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    iniciativa_id = Column(
        String,
        ForeignKey("iniciativas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    descricao = Column(String, nullable=False)
    descricao_vetor = Column(VectorType, nullable=False)
    iniciativa = relationship("Iniciativa", back_populates="descricoes_extras")
