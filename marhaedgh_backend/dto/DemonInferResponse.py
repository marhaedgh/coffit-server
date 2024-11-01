from pydantic import BaseModel

class DemonInferResponse(BaseModel):
    title: str
    keywords: str
    line_summarization: str
    summarization: str
    classification: str
    what_to_do: str