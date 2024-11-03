from sqlalchemy import Column, Integer, Boolean

from db.database import Base

class UserAlertMapping(Base):
    __tablename__ = "user_alert_mapping"

    user_id = Column(Integer, primary_key=True)  # 복합 키
    alert_id = Column(Integer, primary_key=True)  # 복합 키
    is_read = Column(Boolean, default=False)