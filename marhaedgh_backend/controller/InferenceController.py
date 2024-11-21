import logging
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from service.InferenceService import InferenceService
from service.AgentService import AgentService
from dto.BaseResponse import BaseResponse
from dto.InferRequest import InferRequest
from dto.JsonInferRequest import JsonInferRequest
from dto.DemonInferRequest import DemonInferRequest

import ModelLoader

# 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("API Logger")

inferenceService = InferenceService(ModelLoader.InferenceModel())
agentService = AgentService(ModelLoader.InferenceModel())

router = APIRouter(
    prefix="/api/v1/infer",
)

@router.post("", response_model=BaseResponse)
async def inferenceRequest(infer_request: InferRequest):

    logger.info(f"Request Data (Inference): {infer_request.model_dump()}")

    infer_response = await inferenceService.sendInferenceRequest_vLLM(infer_request.role, infer_request.content)

    logger.info(f"Response Data (Inference): {infer_response}")

    return BaseResponse(message="success - inferenceRequest", data=infer_response)


@router.post("/demon", response_model=BaseResponse)
async def demonInferenceRequest(demon_infer_request: DemonInferRequest):

    logger.info(f"Request Data (Demon): {demon_infer_request.model_dump()}")

    demon_infer_response = await agentService.demon_alert_response_efficient(demon_infer_request.url)


    logger.info(f"Response Data (Demon): {demon_infer_response}")

    return BaseResponse(message="success - demon_inferenceRequest", data=demon_infer_response)


@router.post("/json", response_model=BaseResponse)
async def jsonInferenceRequest(json_infer_request: JsonInferRequest):

    logger.info(f"Request Data (JSON): {json_infer_request.model_dump()}")

    json_infer_response = await agentService.json_alert_infer_request(json_infer_request.context)

    logger.info(f"Response Data (JSON): {json_infer_response}")

    return BaseResponse(message="success - json_infer_request", data=json_infer_response)

@router.post("/chat")
async def inference_chatting_request(infer_request: Request):
    data = await infer_request.json()
    question = data["question"]
    prompt = data["prompt"]

    logger.info(f"Request Data (Chat): Question={question}, Prompt={prompt}")

    stream = inferenceService.inference_chatting_streaming(question, prompt)

    logger.info(f"Streaming Response initiated (Chat): Question={question}")

    return StreamingResponse(stream, media_type="text/event-stream")
