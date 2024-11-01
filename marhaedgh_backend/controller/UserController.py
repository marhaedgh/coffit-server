from fastapi import APIRouter

from dto.BaseResponse import BaseResponse
from dto.CreateBusinessRequest import CreateBusinessRequest
from dto.CreateBusinessResponse import CreateBusinessResponse

from service.UserService import UserService

router = APIRouter(
    prefix="/api/v1/user",
)

userService = UserService()


@router.post("/", response_model=CreateBusinessResponse)
async def create_business(req: CreateBusinessRequest):
    res = userService.create_business(req)
    return res