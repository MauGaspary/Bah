from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date, time
from app.enums import HorarioTipo


class TagSchema(BaseModel):
    id: UUID
    nome: str
    descricao: Optional[str]

    class Config:
        orm_mode = True


class OrganizadorSchema(BaseModel):
    id: UUID
    nome: str

    class Config:
        orm_mode = True


class IniciativaHorarioSchema(BaseModel):
    id: UUID
    data_evento: date
    hora_inicio: time
    hora_fim: time
    tipo: HorarioTipo
    criado_em: datetime

    class Config:
        orm_mode = True


class IniciativaSchema(BaseModel):
    id: UUID
    titulo: str
    descricao: str
    descricao_vetor: List[str]
    link: HttpUrl
    destaque: bool
    local: Optional[str]
    imagem_url: HttpUrl
    criado_em: datetime
    editado_em: Optional[datetime]
    deletado_em: Optional[datetime]

    organizador: OrganizadorSchema
    horarios: List[IniciativaHorarioSchema]
    tags: List[TagSchema]

    class Config:
        orm_mode = True
