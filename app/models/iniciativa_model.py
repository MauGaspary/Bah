import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.models.base import Base


class Iniciativa(Base):
    __tablename__ = "iniciativas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    titulo = Column(String, nullable=False, index=True)
    descricao = Column(Text, nullable=False)
    descricao_vetor = Column(Text, nullable=False)
    organizador_id = Column(
        String, ForeignKey("organizadores.id"), nullable=False, index=True
    )
    link = Column(Text, nullable=False)
    destaque = Column(Boolean, nullable=False, default=False, index=True)
    local = Column(String)
    imagem_url = Column(String, nullable=False)

    criado_por = Column(String, ForeignKey("usuarios.id"), nullable=False, index=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    editado_em = Column(DateTime)
    editado_por = Column(String, ForeignKey("usuarios.id"))
    deletado_em = Column(DateTime)
    deletado_por = Column(String, ForeignKey("usuarios.id"))

    organizador = relationship("Organizador", backref="iniciativas")
    horarios = relationship("IniciativaHorario", back_populates="iniciativa")
    tags = relationship("Tag", secondary="iniciativa_tag", backref="iniciativas")
