from typing import List, Dict, Optional, Any

from pydantic import BaseModel


class GetNotificationsResponse(BaseModel):
    id: int
    title: str
    line_summary: str
    keywords: list[str]
    date: str
    is_read: bool