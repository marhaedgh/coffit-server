from fastapi import APIRouter

from dto.BaseResponse import BaseResponse
from dto.GetNotificationsRequest import GetNotificationsRequest
from service.NotificationService import NotificationService

router = APIRouter(
    prefix="/api/v1/notification",
)

notificationService = NotificationService()


@router.get("/", response_model=BaseResponse)
async def get_notifications(
        # TODO: user id required
        get_notifications_request:GetNotificationsRequest
):
    notifications = notificationService.get_notifications(get_notifications_request)
    return BaseResponse(message="success about calling get notifications", data=notifications)


@router.get("/regi", response_model=BaseResponse)
async def get_regi_notifications(
        # TODO: user id required
        get_notifications_request:GetNotificationsRequest
):
    notifications = notificationService.get_regi_after_notifications(get_notifications_request)
    return BaseResponse(message="success about calling get notifications", data=notifications)


@router.get("/{notification_id}", response_model=BaseResponse)
async def get_notification(
        notification_id: int,
):
    notification = notificationService.get_notification(notification_id)
    return BaseResponse(message="success", data=notification)
