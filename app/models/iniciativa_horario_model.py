from datetime import datetime

from sqlalchemy import (
    Column, Date, Time, DateTime, ForeignKey, Enum, String, Index
)
from sqlalchemy.orm import relationship
import uuid
import enum
from app.config.database import Base


class HorarioTipo(enum.Enum):
    presencial = "presencial"
    hibrido = "hibrido"
    online = "online"


class IniciativaHorario(Base):
    __tablename__ = "iniciativa_horarios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    iniciativa_id = Column(String, ForeignKey("iniciativas.id"), nullable=False, index=True)
    data_evento = Column(Date, nullable=False, index=True)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
    tipo = Column(Enum(HorarioTipo), nullable=False)

    __table_args__ = (
        Index("idx_iniciativa_data_evento", "iniciativa_id", "data_evento"),
    )

    iniciativa = relationship("Iniciativa", back_populates="horarios")
