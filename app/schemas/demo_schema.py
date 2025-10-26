from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DemoCreate(BaseModel):
    username: str
    email: str


class DemoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    created_at: datetime
