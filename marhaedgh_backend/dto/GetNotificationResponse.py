from typing import List, Dict, Optional, Any

from pydantic import BaseModel


class GetNotificationResponse(BaseModel):
    id: int
    title: str
    summary: str
    keywords: list[str]
    whattodo: str
    date: str
    content: str = None
