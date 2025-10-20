import email
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserUpdate(BaseModel):
    nome: Optional[str] = Field(None, example="Nome do usuário")
    sobrenome: Optional[str] = Field(None, example="Sobrenome do usuário")
    email: Optional[EmailStr] = Field(None, example="Email do usuário")


class UserResponse(BaseModel):
    id: str
    nome: str
    sobrenome: str
    email: str
    criado_em: datetime

    class config:
        orm_mode = True
