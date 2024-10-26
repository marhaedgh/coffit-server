from fastapi import APIRouter, HTTPException

from service.InferenceService import InferenceService
from dto.InferRequestDto import InferRequestDto

import ModelLoader
 
inferenceService = InferenceService(ModelLoader.InferenceModel())

print(ModelLoader.InferenceModel())

router = APIRouter(
    prefix="/api/v1",
)

@router.post("/infer")
async def inferenceRequest(inferRequestDto:InferRequestDto):

    inferResponseDto = await inferenceService.sendInferenceRequest_vLLM(inferRequestDto.role, inferRequestDto.content)

    return inferResponseDto
