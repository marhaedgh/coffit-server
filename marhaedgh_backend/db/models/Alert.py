from sqlalchemy import Column, Integer, String, JSON, Text, DateTime, Enum

from db.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_data_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    keywords = Column(JSON, nullable=True)
    line_summarization = Column(String, nullable=True)
    text_summarization = Column(Text, nullable=True)
    task_summarization = Column(Text, nullable=True)
    detail_report = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)