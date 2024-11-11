from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from service.InferenceService import InferenceService
from service.AgentService import AgentService
from dto.BaseResponse import BaseResponse
from dto.InferRequest import InferRequest
from dto.DemonInferRequest import DemonInferRequest

import ModelLoader


from llama_index.core import Settings
from util.RBLNBGEM3Embeddings import RBLNBGEM3Embeddings
from llama_index.llms.openai_like import OpenAILike


Settings.embed_model = RBLNBGEM3Embeddings()
Settings.llm = OpenAILike(
    model="rbln_vllm_llama-3-Korean-Bllossom-8B_npu4_batch4_max4096",
    api_base="http://0.0.0.0:8000/v1",
    api_key="1234",
    max_tokens=1024,
    is_chat_model=True
)

 
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


@router.post("/chat-infer")
async def inference_chatting_request(infer_request: Request):
    data = await infer_request.json()
    messages = data["messages"]
    
    # 스트리밍 방식으로 응답 전송
    return StreamingResponse(await inferenceService.inference_chatting_streaming(messages), media_type="text/plain")