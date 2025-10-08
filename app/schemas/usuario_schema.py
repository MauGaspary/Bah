from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UsuarioDelete(BaseModel):
    nome: str
    sobrenome: str
    senha: str
    email: str


class UsuarioResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    nome: str
    sobrenome: str
    email: str
    senha: str
    criado_em: Optional[datetime]
    criado_por: Optional[str]
