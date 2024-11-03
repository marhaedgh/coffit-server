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
    get_notifications_response = notificationService.get_notifications(get_notifications_request)
    return BaseResponse(message="success about calling get notifications", data=get_notifications_response)


@router.get("/regi", response_model=BaseResponse)
async def get_regi_notifications(
        # TODO: user id required
        get_notifications_request:GetNotificationsRequest
):
    get_notifications_response = notificationService.get_regi_after_notifications(get_notifications_request)
    return BaseResponse(message="success about calling get notifications(register)", data=get_notifications_response)


@router.get("/{notification_id}", response_model=BaseResponse)
async def get_notification(
        notification_id: int,
):
    get_notification_response = notificationService.get_notification(notification_id)
    return BaseResponse(message="success", data=get_notification_response)
