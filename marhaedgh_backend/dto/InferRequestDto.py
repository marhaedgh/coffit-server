from pydantic import BaseModel

class InferRequestDto(BaseModel):
    role: str | None = 'User'
    content: str