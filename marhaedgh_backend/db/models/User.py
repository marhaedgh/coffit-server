from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, func

from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_data_id = Column(Integer)  # 외래 키 설정이 필요하지 않으므로 직접 참조
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())