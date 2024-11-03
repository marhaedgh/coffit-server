from sqlalchemy.orm import Session
from sqlalchemy import and_, or_  # and_와 or_를 임포트

from db.models.BusinessData import BusinessData
from db.models.Alert import Alert
from db.models.UserAlertMapping import UserAlertMapping

class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_notification_by_alert_id(self, alert_id: int):
        return self.db.query(Alert).filter(Alert.id == alert_id).first()
    
    def get_notifications_by_user_id(self, user_id: int):
        # alerts_id를 Row 객체에서 실제 ID 값만 리스트로 추출
        alerts_id = [alert.alert_id for alert in self.db.query(UserAlertMapping.alert_id).filter(UserAlertMapping.user_id == user_id).all()]
        
        if not alerts_id:
            return []

        # 해당 alert_id를 가진 alerts 항목 조회
        alerts = self.db.query(Alert).filter(Alert.id.in_(alerts_id)).all()

        return alerts

    

    def get_involved_notifications_by_business_data_id(self, business_data_id: int): 
        # 기준이 되는 business_data 항목 조회
        base_business_data = self.db.query(BusinessData).filter(BusinessData.id == business_data_id).first()
        if not base_business_data:
            return []

        # 복잡한 조인을 통해 business_data와 관련 alert 데이터 가져오기
        alerts = self.db.query(Alert).join(BusinessData, Alert.business_data_id == BusinessData.id).filter(
            and_(
                or_(BusinessData.business_type == base_business_data.business_type, BusinessData.business_type == None),
                or_(BusinessData.corporation_type == base_business_data.corporation_type, BusinessData.corporation_type == None),
                or_(BusinessData.industry == base_business_data.industry, BusinessData.industry == None),
                or_(BusinessData.region == base_business_data.region, BusinessData.region == None),
                or_(BusinessData.representative_birthday == base_business_data.representative_birthday, BusinessData.representative_birthday == None),
                or_(BusinessData.representative_gender == base_business_data.representative_gender, BusinessData.representative_gender == None),
                or_(BusinessData.revenue == base_business_data.revenue, BusinessData.revenue == None),
                or_(BusinessData.employees == base_business_data.employees, BusinessData.employees == None)
            )
        ).all()
        
        return alerts