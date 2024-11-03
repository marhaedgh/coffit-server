from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Enum

from db.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_data_id = Column(Integer, nullable=True)  # 외래 키 설정이 필요하지 않으므로 직접 참조
    title = Column(String(255), nullable=True)
    keywords = Column(Text, nullable=True)  # TEXT 형식
    line_summarization = Column(String(255), nullable=True)
    text_summarization = Column(Text, nullable=True)
    task_summarization = Column(Text, nullable=True)
    detail_report = Column(Text, nullable=True)
    due_date = Column(TIMESTAMP, nullable=True)