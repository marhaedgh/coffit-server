from fastapi import APIRouter, HTTPException

from service.InferenceService import InferenceService

router = APIRouter(
    prefix="/api/v1/",
)

@router.post("/infer")
async def inferenceRequest():



    return result;
