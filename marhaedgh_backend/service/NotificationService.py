from typing import List

from dto.GetNotificationsResponse import GetNotificationsResponse


class NotificationService:
    def get_notifications(self) -> List[GetNotificationsResponse]:
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
                isRead=False
            ),
        ]
