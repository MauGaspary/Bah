from sqlalchemy import (
    Column, Date, Time, TIMESTAMP, ForeignKey, Enum
)
from sqlalchemy.dialects.postgresql import UUID
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

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    iniciativa_id = Column(UUID(as_uuid=True), ForeignKey("iniciativas.id"), nullable=False)
    data_evento = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    criado_em = Column(TIMESTAMP)
    tipo = Column(Enum(HorarioTipo), nullable=False)

    iniciativa = relationship("Iniciativa", back_populates="horarios")
