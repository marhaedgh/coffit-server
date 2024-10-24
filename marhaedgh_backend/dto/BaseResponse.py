from typing import Any, Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):
    message: str
    data: Optional[Any] = None
