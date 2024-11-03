from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, Text, DateTime, Enum

from db.database import Base

# BusinessData 테이블
class BusinessData(Base):
    __tablename__ = "business_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_type = Column(String(255), nullable=True)
    corporation_type = Column(String(255), nullable=True)
    industry = Column(String(255), nullable=True)
    region_city = Column(String(50), nullable=True)
    region_district = Column(String(50), nullable=True)
    representative_birthday = Column(String(10), nullable=True)
    representative_gender = Column(String(10), nullable=True)
    revenue = Column(Float, nullable=True)
    employees = Column(Integer, nullable=True)