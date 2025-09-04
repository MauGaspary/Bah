from sqlalchemy import (
    Column, String, Text, Boolean, TIMESTAMP, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import uuid
from app.config.database import Base


class Iniciativa(Base):
    __tablename__ = "iniciativas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = Column(String, nullable=False)
    descricao = Column(Text, nullable=False)
    descricao_vetor = Column(ARRAY(Text), nullable=False)
    organizador_id = Column(UUID(as_uuid=True), ForeignKey("organizadores.id"), nullable=False)
    link = Column(Text, nullable=False)
    destaque = Column(Boolean, nullable=False)
    local = Column(String)
    imagem_url = Column(Text, nullable=False)

    criado_por = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    criado_em = Column(TIMESTAMP)
    editado_em = Column(TIMESTAMP)
    editado_por = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    deletado_em = Column(TIMESTAMP)
    deletado_por = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))

    organizador = relationship("Organizador", backref="iniciativas")
    horarios = relationship("IniciativaHorario", back_populates="iniciativa")
    tags = relationship("Tag", secondary="iniciativa_tag", backref="iniciativas")
