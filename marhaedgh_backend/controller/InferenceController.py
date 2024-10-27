from fastapi import APIRouter, HTTPException

from service.InferenceService import InferenceService
from service.AgentService import AgentService
from dto.InferRequest import InferRequest
from dto.DemonInferRequest import DemonInferRequest

import ModelLoader
 
inferenceService = InferenceService(ModelLoader.InferenceModel())
agentService = AgentService(ModelLoader.InferenceModel())

router = APIRouter(
    prefix="/api/v1",
)

@router.post("/infer")
async def inferenceRequest(inferRequest:InferRequest):

    inferResponse = await inferenceService.sendInferenceRequest_vLLM(inferRequest.role, inferRequest.content)

    return inferResponse

#URL 넣으면 크롤링해서 alert 테이블 형태와 똑같이 반환
@router.post("/demon-infer")
async def inferenceRequest(demonInferRequest:DemonInferRequest):

    demonInferResponse = await agentService.demonAlertResponse(demonInferRequest.url)

    return demonInferResponse