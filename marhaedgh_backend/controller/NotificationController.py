import logging
from fastapi import APIRouter, HTTPException, Query

from dto.BaseResponse import BaseResponse
from dto.GetNotificationsRequest import GetNotificationsRequest
from service.NotificationService import NotificationService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("API Logger")

router = APIRouter(
    prefix="/api/v1/notification",
)

notificationService = NotificationService()


@router.get("/", response_model=BaseResponse)
async def get_notifications(
        get_notifications_request: GetNotificationsRequest
):

    logger.info(f"Request Data (Get Notifications): {get_notifications_request.model_dump()}")

    notifications = notificationService.get_notifications(get_notifications_request)
    
    logger.info(f"Response Data (Get Notifications): {notifications}")

    return BaseResponse(message="success about calling get notifications", data=notifications)


@router.get("/{notification_id}", response_model=BaseResponse)
async def get_notification(
        notification_id: int,
):

    logger.info(f"Request Data (Get Notification): notification_id={notification_id}")

    notification = notificationService.get_notification(notification_id)

    logger.info(f"Response Data (Get Notification): {notification}")

    return BaseResponse(message="success", data=notification)


@router.patch("/read", response_model=BaseResponse)
async def read_notification(
        user_id: int,
        notification_id: int
):

    logger.info(f"Request Data (Read Notification): user_id={user_id}, notification_id={notification_id}")

    success = notificationService.read_notification(user_id, notification_id)

    if success:
        logger.info("Response Data (Read Notification): Success")
        return BaseResponse(message="success")
    else:
        logger.warning("Response Data (Read Notification): FAIL - missing user-noti mapping.")
        return BaseResponse(message="FAIL : missing user-noti mapping.")
