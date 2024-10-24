from typing import List, Optional

from pydantic import BaseModel


class GetNotificationsResponse(BaseModel):
    title: str
    summary: str
    keywords: List[str]
    date: str
    isRead: bool
    content: Optional[str] = None
