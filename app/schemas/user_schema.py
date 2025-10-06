from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator


class UserCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=100, description="Nome do usuário")
    sobrenome: str = Field(
        min_length=1, max_length=100, description="Sobrenome do usuário"
    )
    email: str = Field(description="Email do usuário")
    password: str = Field(min_length=6, max_length=100, description="Senha do usuário")

    @model_validator(mode="after")
    def validar_email(self):
        if "@" not in self.email or "." not in self.email:
            raise ValueError("Formato de email inválido")
        return self


class UserResponse(BaseModel):
    id: str
    nome: str
    sobrenome: str
    email: str
    criado_em: Optional[datetime] = None
    criado_por: Optional[str] = None
    editado_em: Optional[datetime] = None
    editado_por: Optional[str] = None

    model_config = {"from_attributes": True}
