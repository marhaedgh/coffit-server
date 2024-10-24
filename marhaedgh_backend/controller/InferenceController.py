from fastapi import APIRouter, HTTPException

from service.InferenceService import InferenceService

import ModelLoader

#모델 불러오기
modelLoader = ModelLoader.InferenceModel()
inferenceService = InferenceService(modelLoader)

router = APIRouter(
    prefix="/api/v1",
)

@router.post("/infer")
async def inferenceRequest():

    inferenceService.sendInferenceRequest_vLLM()
    print("안녕 실행 잘 됐어@@@@@@@@@@@@@@@@@@@@@2")
    return 0
