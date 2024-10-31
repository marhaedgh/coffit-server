from typing import List, Dict, Optional, Any

from pydantic import BaseModel


class GetNotificationsResponse(BaseModel):
    id: int
    title: str
    summary: str
    keywords: Optional[Dict[str, Any]]
    date: str
    content: Optional[str] = None
