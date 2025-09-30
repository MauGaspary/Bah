import os
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.models.base import Base

MODEL_DIMENSION = int(os.getenv("MODEL_DIMENSIONS", "768"))

try:
    from pgvector.sqlalchemy import Vector

    VectorType = Vector(MODEL_DIMENSION)
except ImportError:
    VectorType = Text


class Iniciativa(Base):
    __tablename__ = "iniciativas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    titulo = Column(String, nullable=False, index=True)
    descricao = Column(Text, nullable=False)
    descricao_vetor = Column(VectorType, nullable=False)
    organizador_id = Column(
        String, ForeignKey("organizadores.id"), nullable=False, index=True
    )
    link = Column(Text, nullable=False)
    destaque = Column(Boolean, nullable=False, default=False, index=True)
    local = Column(String)
    imagem_url = Column(String, nullable=False)

    criado_por = Column(String, ForeignKey("usuarios.id"), nullable=False, index=True)
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    editado_em = Column(DateTime)
    editado_por = Column(String, ForeignKey("usuarios.id"))
    deletado_em = Column(DateTime)
    deletado_por = Column(String, ForeignKey("usuarios.id"))

    organizador = relationship("Organizador", backref="iniciativas")
    horarios = relationship("IniciativaHorario", back_populates="iniciativa")
    tags = relationship("Tag", secondary="iniciativa_tag", backref="iniciativas")
