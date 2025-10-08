import os
import uuid
from app.models.base import Base
from sqlalchemy import Column, String, Text, ForeignKey
MODEL_DIMENSION = int(os.getenv("MODEL_DIMENSIONS", "768"))

try:
    from pgvector.sqlalchemy import Vector

    VectorType = Vector(MODEL_DIMENSION)
except ImportError:
    VectorType = Text


class DescricoesExtrasModel(Base):
    __tablename__ = "descricoes_extras"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    iniciativa_id = Column(
        String, ForeignKey("iniciativas.id"), nullable=False, index=True
    )
    descricao = Column(String, nullable=False)
    descricao_vetor = Column(VectorType, nullable=False)