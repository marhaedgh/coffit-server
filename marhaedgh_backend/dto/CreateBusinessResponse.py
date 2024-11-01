from pydantic import BaseModel
from datetime import datetime

class CreateBusinessResponse(BaseModel):
    id: int
    username: str
    business_data_id: int
    created_at: datetime
