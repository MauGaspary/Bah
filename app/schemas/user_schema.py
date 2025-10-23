from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator

from app.utils.helpers import validate_email


class UserCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=100, description="Nome do usuário")
    sobrenome: str = Field(
        min_length=1, max_length=100, description="Sobrenome do usuário"
    )
    email: str = Field(description="Email do usuário")
    password: str = Field(min_length=6, max_length=100, description="Senha do usuário")

    @model_validator(mode="after")
    def validar_email(self):
        if not validate_email(self.email):
            raise ValueError("Formato de email inválido")
        return self


class UserUpdate(BaseModel):
    nome: Optional[str] = Field(None, example="Nome do usuário")
    sobrenome: Optional[str] = Field(None, example="Sobrenome do usuário")
    email: Optional[EmailStr] = Field(None, example="Email do usuário")


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