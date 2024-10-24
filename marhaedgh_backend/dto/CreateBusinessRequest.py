from typing import List

from pydantic import BaseModel

from enumeration.BusinessType import BusinessType
from enumeration.CorporationType import CorporationType
from enumeration.Industry import Industry


class CreateBusinessRequest(BaseModel):
    business_type: BusinessType
    corporation_type: List[CorporationType]
    industry: Industry
    region: str
    representative_birthday: str  # YYYY-MM-DD
    representative_gender: str  # '남' 또는 '여'
    revenue: float
    employees: int
