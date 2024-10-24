from fastapi import APIRouter

from dto.BaseResponse import BaseResponse
from service.NotificationService import NotificationService

router = APIRouter(
    prefix="/api/v1/notification",
)

notificationService = NotificationService()


@router.get("/", response_model=BaseResponse)
async def get_notifications(
        # TODO: user id required
):
    notifications = notificationService.get_notifications()
    return BaseResponse(message="success", data=notifications)


@router.patch("/read", response_model=BaseResponse)
async def read_notification(
        notification_id: int
):
    notificationService.read_notification(notification_id)
    return BaseResponse(message="success")


@router.get("/{notification_id}", response_model=BaseResponse)
async def get_notification(
        notification_id: int,
):
    notification = notificationService.get_notification(notification_id)
    return BaseResponse(message="success", data=notification)
