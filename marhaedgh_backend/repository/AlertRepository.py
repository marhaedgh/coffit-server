from sqlalchemy.orm import Session
from db.models.Alert import Alert
from typing import List

class AlertRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, alert_data: dict) -> Alert:
        alert = Alert(**alert_data)
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def get_by_id(self, alert_id: int) -> Alert:
        return self.db.query(Alert).filter(Alert.id == alert_id).first()

    def get_all(self) -> List[Alert]:
        return self.db.query(Alert).all()

    def update(self, alert_id: int, update_data: dict) -> Alert:
        alert = self.get_by_id(alert_id)
        if alert:
            for key, value in update_data.items():
                setattr(alert, key, value)
            self.db.commit()
            self.db.refresh(alert)
        return alert

    def delete(self, alert_id: int) -> None:
        alert = self.get_by_id(alert_id)
        if alert:
            self.db.delete(alert)
            self.db.commit()
