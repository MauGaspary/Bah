from datetime import date, datetime, time
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator

from app.models.iniciativa_horario_model import HorarioTipo
from app.schemas.admin_iniciativa_schemas import IniciativaFiltersSchema


class IniciativaHorarioCreate(BaseModel):
    data_evento: date = Field(description="Data do evento")
    hora_inicio: time = Field(description="Horário de início")
    hora_fim: time = Field(description="Horário de fim")
    tipo: HorarioTipo = Field(description="Tipo do horário")

    @model_validator(mode="after")
    def validar_horarios(self):
        if self.hora_fim <= self.hora_inicio:
            raise ValueError("Hora de fim deve ser maior que hora de início")
        return self


class IniciativaCreate(BaseModel):
    titulo: str = Field(
        min_length=1, max_length=255, description="Título da iniciativa"
    )
    descricao: str = Field(min_length=1, description="Descrição da iniciativa")
    organizador_id: str = Field(description="ID do organizador")
    link: str = Field(description="Link da iniciativa")
    local: Optional[str] = Field(
        None, max_length=255, description="Local da iniciativa"
    )
    imagem_url: str = Field(description="URL da imagem")
    destaque: bool = Field(False, description="Se a iniciativa é destaque")
    horarios: List[IniciativaHorarioCreate] = Field(
        min_length=1, description="Lista de horários da iniciativa"
    )
    tag_ids: Optional[List[str]] = Field(None, description="Lista de IDs das tags")
    descricoes_extras: Optional[List[str]] = Field(
        default=None, description="Lista de descrições extras"
    )


class IniciativaHorarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    data_evento: date
    hora_inicio: time
    hora_fim: time
    tipo: HorarioTipo
    criado_em: Optional[datetime] = None


class IniciativaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    titulo: str
    descricao: str
    organizador_id: Optional[str] = None
    link: str
    local: Optional[str] = None
    imagem_url: str
    destaque: bool
    horarios: List[IniciativaHorarioResponse]
    criado_em: Optional[datetime] = None
    criado_por: Optional[str] = None
    editado_em: Optional[datetime] = None
    editado_por: Optional[str] = None


class IniciativaListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: List[IniciativaResponse]
    total: int
    filters: IniciativaFiltersSchema
