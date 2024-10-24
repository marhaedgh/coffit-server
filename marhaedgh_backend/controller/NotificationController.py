from fastapi import APIRouter

from dto.BaseResponse import BaseResponse
from service.NotificationService import NotificationService

router = APIRouter(
    prefix="/api/v1/notification",
)

notificationService = NotificationService()


@router.post("/", response_model=BaseResponse)
async def get_notifications(
        # TODO: user id required
):
    notifications = notificationService.get_notifications()
    return BaseResponse(message="success", data=notifications)
