from pydantic import BaseModel


class OrganizadorCreate(BaseModel):
    nome: str


class OrganizadorUpdate(BaseModel):
    nome: str | None = None


class OrganizadorResponse(BaseModel):

    id: str
    nome: str

    model_config = {"from_attributes": True}
