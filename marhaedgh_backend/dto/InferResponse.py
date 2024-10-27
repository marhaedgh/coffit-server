from pydantic import BaseModel

class InferResponse(BaseModel):
    result: str