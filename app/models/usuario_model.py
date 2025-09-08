import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text

from app.config.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    nome = Column(String, nullable=False)
    sobrenome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    senha_hash = Column(Text, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
