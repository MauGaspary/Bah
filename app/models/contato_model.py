from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.config.database import Base


class Contato(Base):
    __tablename__ = "contatos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    assunto = Column(String, nullable=False)
    mensagem = Column(Text, nullable=False)
    enviado_em = Column(TIMESTAMP)
