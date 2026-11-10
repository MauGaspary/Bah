from pydantic import BaseModel


class TagCreate(BaseModel):
    nome: str
    descricao: str | None = None


class TagUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None


class TagResponse(BaseModel):

    id: str
    nome: str
    descricao: str | None

    model_config = {"from_attributes": True}
