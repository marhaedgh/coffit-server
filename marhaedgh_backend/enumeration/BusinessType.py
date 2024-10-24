from enum import Enum


class BusinessType(str, Enum):
    개인사업자 = "개인사업자"
    법인사업자 = "법인사업자"
