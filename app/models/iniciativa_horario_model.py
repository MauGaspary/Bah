import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Index, String, Time
from sqlalchemy.orm import relationship

from app.models.base import Base


class HorarioTipo(enum.Enum):
    PRESENCIAL = "presencial"
    HIBRIDO = "hibrido"
    ONLINE = "online"


class IniciativaHorario(Base):
    __tablename__ = "iniciativa_horarios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    iniciativa_id = Column(
        String, ForeignKey("iniciativas.id"), nullable=False, index=True
    )
    data_evento = Column(Date, nullable=False, index=True)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
    tipo = Column(Enum(HorarioTipo), nullable=False)

    __table_args__ = (
        Index("idx_iniciativa_data_evento", "iniciativa_id", "data_evento"),
    )

    iniciativa = relationship("Iniciativa", back_populates="horarios")
