from typing import List
import json

from db.database import get_db

from dto.GetNotificationsRequest import GetNotificationsRequest
from dto.GetNotificationsResponse import GetNotificationsResponse

from repository.NotificationRepository import NotificationRepository


class NotificationService:
    def get_notifications(self, get_notifications_request: GetNotificationsRequest) -> List[GetNotificationsResponse]:
        # TODO: 사용자 매핑 분류 정보 불러오기 -> USER_id 필요
        #       ㄴ 가입시 클라이언트에게 user_id넘겨주고, 가지고 있게하기.
        #       ㄴ notification 보내기 위해 userid GetNotificationsRequest에 UserID 포함
        db: Session = next(get_db())
        # 일단 지금은 request에 businessDataId 받았으니 바로 businessData에서 분류 검색 수행
        # TODO: ㄴ UserID로 DB에서 사용자의 분류 가져오기 ( 사용자테이블에서 businessid -> 검색해서 분류)
        # TODO: 해당 분류에 해당하는 Notifications 가져오기
        #       ㄴ Notification은 정확히 한 분류로 들어가지 않음. 즉 조건이 몇가지만 있고 나머진 조건에 해당하지 않음. 따라서 조건없음 == none
        # TODO: ㄴ 조건에 맞으면 list로 전부 가져오는 쿼리 작성
        notification_repository = NotificationRepository(db)
        alerts = notification_repository.get_involved_notifications_by_business_data_id(
            get_notifications_request.business_data_id
        )

        response_list = []
    
        for alert in alerts:
            # GetNotificationsResponse에 맞게 데이터 변환
            response = GetNotificationsResponse(
                id=alert.id,
                title=alert.title,
                summary=alert.line_summarization,
                keywords=alert.keywords,
                #keywords=alert.keywords if alert.keywords else [],  # keywords가 None일 경우 빈 리스트 반환
                date=alert.due_date.strftime("%Y-%m-%d") if alert.due_date else "",  # 날짜 포맷 지정
                content=alert.text_summarization
            )
            response_list.append(response)
        
        return response_list

        #       ㄴ return GetNotificationResponse
        # TODO: GetNotificationsResponse에 넣어 정리 후 넘기기

        """

        return [
            # NOTE: dummy
            GetNotificationsResponse(
                title="최저 시급 인상",
                summary="2025년부터 최저 시급이 2만원으로 인상됩니다.",
                keywords=["키워드1", "키워드2"],
                date="2021-07-01",
                isRead=False
            ),
            GetNotificationsResponse(
                title="사회적 거리두기 시행",
                summary="코로나19 확진자가 급증으로 사회적 거리두기 4단계가 시행됩니다.",
                keywords=["키워드1", "키워드2"],
                date="2021-07-01",
                isRead=False
            ),
            GetNotificationsResponse(
                title="주휴수당 폐지",
                summary="이제 알바생 한 명이 많은 시간 일해도 딱 시급만큼만 받습니다.",
                keywords=["키워드1", "키워드2"],
                date="2021-07-01",
                isRead=True
            ),
        ]

    def get_notification(self, notification_id: int) -> str:
        return # 사업 성공을 위한 핵심 전략

안녕하세요, 사업자 여러분! 오늘은 **사업 성공을 위한 핵심 전략**에 대해 알아보겠습니다.

## 1. 고객 중심 사고

모든 성공적인 사업의 핵심은 *고객*입니다. 다음 사항을 항상 명심하세요:

- 고객의 니즈 파악하기
- 고객 피드백 적극 수용하기
- 지속적인 고객 서비스 개선

## 2. 효과적인 마케팅 전략

좋은 제품이나 서비스도 **효과적인 마케팅**이 없으면 빛을 발하기 어렵습니다.

1. 타겟 고객 명확히 정의하기
2. 다양한 마케팅 채널 활용하기
3. 콘텐츠 마케팅 강화하기

## 3. 재무 관리의 중요성

안정적인 *재무 관리*는 사업의 지속 가능성을 보장합니다.

> "수익은 허영심을 만족시키지만, 현금 흐름은 생존을 보장한다." - 알 수 없음

## 4. 지속적인 학습과 혁신

시장은 계속 변화합니다. **지속적인 학습**과 *혁신*만이 경쟁에서 살아남을 수 있는 길입니다.

더 자세한 정보는 [중소벤처기업부 홈페이지](https://www.mss.go.kr/)를 참고하세요.

### 마무리

이상으로 사업 성공을 위한 핵심 전략에 대해 알아보았습니다. 항상 고객을 생각하고, 효과적으로 마케팅하며, 재무를 철저히 관리하고, 끊임없이 학습하고 혁신하는 자세를 가집시다!

**화이팅!** 🚀
"""