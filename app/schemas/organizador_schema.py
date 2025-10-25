from pydantic import BaseModel


class OrganizadorResponse(BaseModel):
    """Schema para resposta de um organizador."""

    id: str
    nome: str

    model_config = {"from_attributes": True}
