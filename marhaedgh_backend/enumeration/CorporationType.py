from enum import Enum


class CorporationType(str, Enum):
    창업 = "창업"
    재창업 = "재창업"
    기존사업자 = "기존 사업자"
