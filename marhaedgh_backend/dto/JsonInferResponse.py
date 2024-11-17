from pydantic import BaseModel

class JsonInferResponse(BaseModel):
    title: str
    keywords: str
    line_summarization: str
    summarization: str
    what_to_do: str