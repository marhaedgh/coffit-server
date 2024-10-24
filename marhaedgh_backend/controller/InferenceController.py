from fastapi import APIRouter, HTTPException

from service.InferenceService import InferenceService
from dto.InferRequestDto import InferRequestDto

import ModelLoader

#모델 불러오기
modelLoader = ModelLoader.InferenceModel()
inferenceService = InferenceService(modelLoader)

router = APIRouter(
    prefix="/api/v1",
)

@router.post("/infer")
async def inferenceRequest(inferRequestDto:InferRequestDto):

    inferResponseDto = await inferenceService.sendInferenceRequest_vLLM(inferRequestDto.role, inferRequestDto.content)

    return inferResponseDto
