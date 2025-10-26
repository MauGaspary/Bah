from datetime import date, datetime, time
from enum import Enum
from typing import List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    field_validator,
    model_validator,
)

from app.models.iniciativa_horario_model import HorarioTipo


class TagSchema(BaseModel):
    """Schema para representação de tag."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    nome: str
    descricao: Optional[str] = None


class OrganizadorSchema(BaseModel):
    """Schema para representação de organizador."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    nome: str


class DescricoesExtrasSchema(BaseModel):
    """Schema para descrições extras de iniciativa."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    descricao: str


class IniciativaFiltersSchema(BaseModel):
    """Schema para filtros de listagem de iniciativas."""

    q: Optional[str] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
    order_by: str = "criado_em"
    order_dir: str = "desc"
    page: int = 1
    size: int = 10


class IniciativaHorarioCreate(BaseModel):
    """Schema para criar um horário de iniciativa."""

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
    """Schema para criar uma nova iniciativa."""

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


class IniciativaHorarioPatch(BaseModel):
    """Schema para atualização parcial de horário."""

    data_evento: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fim: Optional[time] = None
    tipo: Optional[HorarioTipo] = None

    @field_validator("hora_fim")
    @classmethod
    def _fim_depois_de_inicio(cls, v, info):
        inicio = info.data.get("hora_inicio")
        if v and inicio and v <= inicio:
            raise ValueError("hora_fim deve ser maior que hora_inicio")
        return v

    @field_validator("data_evento")
    @classmethod
    def _nao_retroativa(cls, v):
        if v and v < date.today():
            raise ValueError("data_evento não pode ser retroativa")
        return v


class DescricaoExtraUpdateSchema(BaseModel):
    """Schema para atualização de descrição extra."""

    id: str
    descricao: str


class IniciativaPatchSchema(BaseModel):
    """Schema para atualização parcial de iniciativa."""

    titulo: Optional[str] = None
    descricao: Optional[str] = None
    link: Optional[str] = None
    destaque: Optional[bool] = None
    local: Optional[str] = None
    imagem_url: Optional[str] = None
    organizador_id: Optional[str] = None

    tags_ids: Optional[List[str]] = None
    horarios: Optional[List[IniciativaHorarioPatch]] = None
    descricoes_extras_update: Optional[List[DescricaoExtraUpdateSchema]] = None
    descricoes_extras_delete_ids: Optional[List[str]] = None
    descricoes_extras_add: Optional[List[str]] = None


class IniciativaHorarioResponse(BaseModel):
    """Schema de resposta para horário de iniciativa (simples)."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    data_evento: date
    hora_inicio: time
    hora_fim: time
    tipo: HorarioTipo
    criado_em: Optional[datetime] = None


class IniciativaHorarioSchema(BaseModel):
    """Schema completo de horário (usado pelo schema admin)."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    data_evento: date
    hora_inicio: time
    hora_fim: time
    tipo: HorarioTipo
    criado_em: datetime


class IniciativaResponse(BaseModel):
    """Schema de resposta básico de iniciativa (endpoints públicos)."""

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

    organizador: Optional[OrganizadorSchema] = None
    tags: Optional[List[TagSchema]] = None
    descricoes_extras: Optional[List[DescricoesExtrasSchema]] = None


class IniciativaSchema(BaseModel):
    """Schema completo de iniciativa (usado por endpoints admin)."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    titulo: str
    descricao: str
    link: str
    destaque: bool
    local: Optional[str]
    imagem_url: str
    organizador_id: Optional[str]
    criado_por: str
    criado_em: datetime
    editado_em: Optional[datetime] = None
    editado_por: Optional[str] = None
    deletado_em: Optional[datetime] = None
    deletado_por: Optional[str] = None

    organizador: Optional[OrganizadorSchema]
    horarios: List[IniciativaHorarioSchema]
    tags: List[TagSchema]
    descricoes_extras: List[DescricoesExtrasSchema]


class IniciativaListResponse(BaseModel):
    """Schema de resposta para listagem básica (busca semântica)."""

    model_config = ConfigDict(from_attributes=True)

    items: List[IniciativaResponse]
    total: int
    filters: IniciativaFiltersSchema


class IniciativaListResponseSchema(BaseModel):
    """Schema de resposta para listagem admin (com filtros completos)."""

    model_config = ConfigDict(from_attributes=True)

    items: List[IniciativaSchema]
    total: int
    filters: IniciativaFiltersSchema


class CalendarioHorarioTipo(str, Enum):
    """Enum para tipo de horário no calendário."""

    PRESENCIAL = "PRESENCIAL"
    ONLINE = "ONLINE"
    HIBRIDO = "HIBRIDO"


class CalendarioIniciativaItem(BaseModel):
    """Schema para item de iniciativa no calendário."""

    iniciativa_id: str
    horario_id: str
    titulo: str
    descricao: str
    hora_inicio: time
    hora_fim: time
    tipo: CalendarioHorarioTipo
    link: str
    local: Optional[str] = None
    imagem_url: str
    destaque: bool
    tags: List[TagSchema] = []


class DiaCalendario(BaseModel):
    """Schema para um dia no calendário."""

    data: date
    iniciativas: List[CalendarioIniciativaItem]


class CalendarioMensalResponse(BaseModel):
    """Schema de resposta para calendário mensal."""

    mes: str
    dias: List[DiaCalendario]
