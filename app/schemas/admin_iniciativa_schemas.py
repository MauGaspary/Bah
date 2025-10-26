from datetime import date, datetime, time
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from app.models.iniciativa_horario_model import HorarioTipo


class descricoesExtrasSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    descricao: str


class TagSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nome: str
    descricao: Optional[str]


class OrganizadorSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nome: str


class IniciativaHorarioSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    data_evento: date
    hora_inicio: time
    hora_fim: time
    tipo: HorarioTipo
    criado_em: datetime


class IniciativaSchema(BaseModel):
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
    descricoes_extras: List[descricoesExtrasSchema]


class IniciativaFiltersSchema(BaseModel):
    q: Optional[str] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
    order_by: str = "criado_em"
    order_dir: str = "desc"
    page: int = 1
    size: int = 10


class IniciativaListResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: List[IniciativaSchema]
    total: int
    filters: IniciativaFiltersSchema


class IniciativaHorarioPatch(BaseModel):
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
    id: str
    descricao: str


class IniciativaPatchSchema(BaseModel):
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
