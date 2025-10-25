from pydantic import BaseModel


class OrganizadorResponse(BaseModel):

    id: str
    nome: str

    model_config = {"from_attributes": True}
