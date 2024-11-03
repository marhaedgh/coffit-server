from pydantic import BaseModel
from datetime import datetime

class CreateBusinessResponse(BaseModel):
    user_id: int
    business_data_id: int
