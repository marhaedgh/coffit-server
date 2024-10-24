from fastapi import APIRouter

from dto.BaseResponse import BaseResponse
from dto.CreateBusinessRequest import CreateBusinessRequest
from service.UserService import UserService

router = APIRouter(
    prefix="/api/v1/user",
)

userService = UserService()


@router.post("/", response_model=BaseResponse)
async def create_business(req: CreateBusinessRequest):
    userService.create_business(req)
    return BaseResponse(message="success")
