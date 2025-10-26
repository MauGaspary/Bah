from pydantic import BaseModel


class TagResponse(BaseModel):

    id: str
    nome: str
    descricao: str | None

    model_config = {"from_attributes": True}
