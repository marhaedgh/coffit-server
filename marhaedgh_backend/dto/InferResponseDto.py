from pydantic import BaseModel

class InferResponseDto(BaseModel):
    result: str