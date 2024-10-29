from sqlalchemy.orm import Session
from db.models.UserAlertMapping import UserAlertMapping

class UserAlertMappingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_alert_mapping_data: dict) -> UserAlertMapping:
        mapping = UserAlertMapping(**user_alert_mapping_data)
        self.db.add(mapping)
        self.db.commit()
        self.db.refresh(mapping)
        return mapping

    def get_by_user_and_alert(self, user_id: int, alert_id: int) -> UserAlertMapping:
        return self.db.query(UserAlertMapping).filter(
            UserAlertMapping.user_id == user_id,
            UserAlertMapping.alert_id == alert_id
        ).first()

    def delete(self, user_id: int, alert_id: int) -> None:
        mapping = self.get_by_user_and_alert(user_id, alert_id)
        if mapping:
            self.db.delete(mapping)
            self.db.commit()
