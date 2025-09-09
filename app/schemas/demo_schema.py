from datetime import datetime

from pydantic import BaseModel


class DemoCreate(BaseModel):
    username: str
    email: str


class DemoResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}
