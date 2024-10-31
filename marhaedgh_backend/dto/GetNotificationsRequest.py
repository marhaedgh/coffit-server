from typing import List, Optional

from pydantic import BaseModel


class GetNotificationsRequest(BaseModel):
    user_id: int
    business_data_id: int #user_id 저장할 때 business_data_id도 가지고있으면 쿼리 한 번 덜 치긴해서 더 효율적이지 않을까?
