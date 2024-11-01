from sqlalchemy import Column, Integer

from db.database import Base

class UserAlertMapping(Base):
    __tablename__ = "user_alert_mapping"

    user_id = Column(Integer, primary_key=True)
    alert_id = Column(Integer, primary_key=True)