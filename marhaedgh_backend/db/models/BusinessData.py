from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, Text, DateTime, Enum

from db.database import Base

class BusinessData(Base):
    __tablename__ = "business_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_type = Column(String, nullable=True)
    corporation_type = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    region = Column(String, nullable=True)
    representative_birthday = Column(String, nullable=True)  # 날짜 형식으로 저장하려면 Date로 변경 가능
    representative_gender = Column(String, nullable=True)
    revenue = Column(Integer, nullable=True)
    employees = Column(Integer, nullable=True)