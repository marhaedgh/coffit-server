from enum import Enum


class CorporationType(str, Enum):
    개인법인_동일 = "개인법인 동일"
    창업 = "창업"
    재창업 = "재창업"
    기존사업자 = "기존 사업자"
