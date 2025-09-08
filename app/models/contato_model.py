import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text

from app.config.database import Base


class Contato(Base):
    __tablename__ = "contatos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    assunto = Column(String, nullable=False)
    mensagem = Column(Text, nullable=False)
    enviado_em = Column(DateTime, default=datetime.utcnow)
