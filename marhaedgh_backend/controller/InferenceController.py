from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
import asyncio

from service.InferenceService import InferenceService
from service.AgentService import AgentService
from dto.BaseResponse import BaseResponse
from dto.InferRequest import InferRequest
from dto.JsonInferRequest import JsonInferRequest
from dto.DemonInferRequest import DemonInferRequest

import ModelLoader

 
inferenceService = InferenceService(ModelLoader.InferenceModel())
agentService = AgentService(ModelLoader.InferenceModel())

router = APIRouter(
    prefix="/api/v1/infer",
)

@router.post("", response_model=BaseResponse)
async def inferenceRequest(infer_request:InferRequest):

    infer_response = await inferenceService.sendInferenceRequest_vLLM(infer_request.role, infer_request.content)

    return BaseResponse(message="success - inferenceRequest", data=infer_response)
    

#URL 넣으면 크롤링해서 alert 테이블 형태와 똑같이 반환
@router.post("/demon", response_model=BaseResponse)
async def demonInferenceRequest(demon_infer_request:DemonInferRequest):

    demon_infer_response = await agentService.demon_alert_response_efficient(demon_infer_request.url)

    return BaseResponse(message="success - demon_inferenceRequest", data=demon_infer_response)


#Json 넣으면 alert 테이블 형태와 똑같이 반환
@router.post("/json", response_model=BaseResponse)
async def jsonInferenceRequest(json_infer_request:JsonInferRequest):

    json_infer_response = await agentService.json_alert_infer_request(json_infer_request.context)

    return BaseResponse(message="success - json_infer_request", data=json_infer_response)


@router.post("/chat")
async def inference_chatting_request(infer_request: Request):
    data = await infer_request.json()
    question = data["question"]
    prompt = data["prompt"]
    
    # 스트리밍 방식으로 응답 전송
    return StreamingResponse(await inferenceService.inference_chatting_streaming(question, prompt), media_type="text/event-stream")