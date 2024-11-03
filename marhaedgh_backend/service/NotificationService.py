from typing import List
import json

from db.database import get_db

from dto.GetNotificationsRequest import GetNotificationsRequest
from dto.GetNotificationsResponse import GetNotificationsResponse
from dto.GetNotificationResponse import GetNotificationResponse

from repository.NotificationRepository import NotificationRepository


class NotificationService:

    def get_notification(self, alert_id: int):
        db: Session = next(get_db())

        notification_repository = NotificationRepository(db)

        alert = notification_repository.get_notification_by_alert_id(alert_id)

        return GetNotificationResponse(
            id = alert.id,
            title = alert.title,
            summary = alert.line_summarization,
            keywords = alert.keywords.split(","),
            whattodo = alert.task_summarization,
            date = alert.due_date.strftime("%Y-%m-%d") if alert.due_date else "",  # 날짜 포맷 지정
            content = alert.text_summarization
        )


    def get_notifications(self, get_notifications_request: GetNotificationsRequest) -> List[GetNotificationsResponse]:
        # user, alert mapping repo 이용한 api
        db: Session = next(get_db())

        notification_repository = NotificationRepository(db)
        alerts = notification_repository.get_notifications_by_user_id(
            get_notifications_request.user_id
        )

        response_list = []

        for alert in alerts:
            # GetNotificationsResponse에 맞게 데이터 변환
            response = GetNotificationsResponse(
                id=alert.id,
                title=alert.title,
                line_summary=alert.line_summarization,
                keywords=alert.keywords.split(",") if alert.keywords else [], # keywords가 None일 경우 빈 리스트 반환 
                date=alert.due_date.strftime("%Y-%m-%d") if alert.due_date else "",  # 날짜 포맷 지정
                is_read=notification_repository.get_is_read_by_ids(get_notifications_request.user_id, alert.id)
            )
            response_list.append(response)
            
        return response_list

    def read_notification(self, user_id: int, notification_id: int):
        db: Session = next(get_db())

        notification_repository = NotificationRepository(db)
        if notification_repository.change_read_true(user_id, notification_id):
            return True
        else:
            return False
        



    def get_notifications_by_business_data(self, get_notifications_request: GetNotificationsRequest) -> List[GetNotificationsResponse]:
        # 우리가 가진 데이터 전부에서 검색해서 제공하는 api
        # TODO: 사용자 매핑 분류 정보 불러오기 -> USER_id 필요
        #       ㄴ 가입시 클라이언트에게 user_id넘겨주고, 가지고 있게하기.
        #       ㄴ notification 보내기 위해 userid GetNotificationsRequest에 UserID 포함
        # 일단 지금은 request에 businessDataId 받았으니 바로 businessData에서 분류 검색 수행
        # TODO: ㄴ UserID로 DB에서 사용자의 분류 가져오기 ( 사용자테이블에서 businessid -> 검색해서 분류)
        # TODO: 해당 분류에 해당하는 Notifications 가져오기
        #       ㄴ Notification은 정확히 한 분류로 들어가지 않음. 즉 조건이 몇가지만 있고 나머진 조건에 해당하지 않음. 따라서 조건없음 == none
        # TODO: ㄴ 조건에 맞으면 list로 전부 가져오는 쿼리 작성
        db: Session = next(get_db())

        notification_repository = NotificationRepository(db)
        alerts = notification_repository.get_notifications_by_business_data_id(
            get_notifications_request.business_data_id
        )

        response_list = []
    
        for alert in alerts:
            # GetNotificationsResponse에 맞게 데이터 변환
            response = GetNotificationsResponse(
                id=alert.id,
                title=alert.title,
                line_summary=alert.line_summarization,
                keywords=alert.keywords.split(",") if alert.keywords else [], # keywords가 None일 경우 빈 리스트 반환 
                date=alert.due_date.strftime("%Y-%m-%d") if alert.due_date else "",  # 날짜 포맷 지정
            )
            response_list.append(response)
        
        return response_list

        #       ㄴ return GetNotificationResponse
        # TODO: GetNotificationsResponse에 넣어 정리 후 넘기기