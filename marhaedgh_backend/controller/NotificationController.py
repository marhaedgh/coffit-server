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
    #notifications = notificationService.get_notifications_by_business_data(get_notifications_request)
    return BaseResponse(message="success about calling get notifications", data=notifications)


@router.get("/{notification_id}", response_model=BaseResponse)
async def get_notification(
        notification_id: int,
):
    notification = notificationService.get_notification(notification_id)
    return BaseResponse(message="success", data=notification)


@router.patch("/read", response_model=BaseResponse)
async def read_notification(
        user_id: int,
        notification_id: int
):
    if notificationService.read_notification(user_id, notification_id):
        return BaseResponse(message="success")
    else:
        return BaseResponse(message="FAIL : missing user-noti mapping.")
