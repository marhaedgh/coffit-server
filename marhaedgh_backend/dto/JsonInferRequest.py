from pydantic import BaseModel
from typing import Any, Dict

class JsonInferRequest(BaseModel):
    context: Dict[str, Any]