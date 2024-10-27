from pydantic import BaseModel

class InferRequest(BaseModel):
    role: str | None = 'User'
    content: str