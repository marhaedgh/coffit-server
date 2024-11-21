import logging
from fastapi import APIRouter
from dto.BaseResponse import BaseResponse
from dto.CreateBusinessRequest import CreateBusinessRequest
from dto.CreateBusinessResponse import CreateBusinessResponse

from service.AgentService import AgentService
from service.UserService import UserService

import ModelLoader


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("API Logger")

router = APIRouter(
    prefix="/api/v1/user",
)

userService = UserService()
agentService = AgentService(ModelLoader.InferenceModel())


@router.post("/", response_model=BaseResponse)
async def create_business(req: CreateBusinessRequest):

    logger.info(f"Request Data (Create Business): {req.model_dump()}")

    create_business_response = userService.create_business(req)

    await agentService.initial_mapping_notifications(create_business_response)

    logger.info(f"Response Data (Create Business): {create_business_response}")

    return BaseResponse(message="success - create_business", data=create_business_response)
