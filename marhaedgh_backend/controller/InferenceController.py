from fastapi import APIRouter, HTTPException

from service.InferenceService import InferenceService
from service.AgentService import AgentService
from dto.BaseResponse import BaseResponse
from dto.InferRequest import InferRequest
from dto.DemonInferRequest import DemonInferRequest

import ModelLoader
 
inferenceService = InferenceService(ModelLoader.InferenceModel())
agentService = AgentService(ModelLoader.InferenceModel())

router = APIRouter(
    prefix="/api/v1",
)

@router.post("/infer", response_model=BaseResponse)
async def inferenceRequest(infer_request:InferRequest):

    infer_response = await inferenceService.sendInferenceRequest_vLLM(infer_request.role, infer_request.content)

    return BaseResponse(message="success - inferenceRequest", data=infer_response)
    

#URL 넣으면 크롤링해서 alert 테이블 형태와 똑같이 반환
@router.post("/demon-infer", response_model=BaseResponse)
async def inferenceRequest(demon_infer_request:DemonInferRequest):

    demon_infer_response = await agentService.demon_alert_response_efficient(demon_infer_request.url)

    return BaseResponse(message="success - demon_inferenceRequest", data=demon_infer_response)