from datetime import date, datetime, time
from typing import List, Optional

from pydantic import BaseModel

from app.models.iniciativa_horario_model import HorarioTipo


class TagSchema(BaseModel):
    id: str
    nome: str
    descricao: Optional[str]

    class Config:
        from_attributes = True


class OrganizadorSchema(BaseModel):
    id: str
    nome: str

    class Config:
        from_attributes = True


class IniciativaHorarioSchema(BaseModel):
    id: str
    data_evento: date
    hora_inicio: time
    hora_fim: time
    tipo: HorarioTipo
    criado_em: datetime

    class Config:
        from_attributes = True


class IniciativaSchema(BaseModel):
    id: str
    titulo: str
    descricao: str
    descricao_vetor: str
    link: str
    destaque: bool
    local: Optional[str]
    imagem_url: str
    organizador_id: str
    criado_por: str
    criado_em: datetime
    editado_em: Optional[datetime] = None
    editado_por: Optional[str] = None
    deletado_em: Optional[datetime] = None
    deletado_por: Optional[str] = None

    organizador: OrganizadorSchema
    horarios: List[IniciativaHorarioSchema]
    tags: List[TagSchema]

    class Config:
        from_attributes = True


class IniciativaFiltersSchema(BaseModel):
    q: Optional[str] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
    order_by: str = "criado_em"
    order_dir: str = "desc"
    page: int = 1
    size: int = 10


class IniciativaListResponseSchema(BaseModel):
    items: List[IniciativaSchema]
    total: int
    filters: IniciativaFiltersSchema

    class Config:
        from_attributes = True
