from typing import List, Dict, Optional, Any

from pydantic import BaseModel


class GetNotificationResponse(BaseModel):
    id: int
    title: str
    summary: str
    keywords: Optional[Dict[str, Any]]
    whattodo: str
    date: str
    content: Optional[str] = None
