from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    business_data_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)