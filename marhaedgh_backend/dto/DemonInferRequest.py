from pydantic import BaseModel

class DemonInferRequest(BaseModel):
    url: str