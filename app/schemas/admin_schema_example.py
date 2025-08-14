from pydantic import BaseModel
from datetime import datetime

class AdminCreate(BaseModel):
    username: str
    email: str

class AdminResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    model_config = {"from_attributes": True}