import asyncio
from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams

from dto.InferResponseDto import InferResponseDto

class InferenceService:

    def __init__(self, modelLoader):
        self.modelLoader = modelLoader

    def sendInferenceRequest_gRPC(self):

        #gRPC Client ver
        return 0

    async def sendInferenceRequest_vLLM(self, role, content):
        # vllm serving ver
        sampling_params = SamplingParams(
            temperature=0.0,
            skip_special_tokens=True,
            stop_token_ids=self.modelLoader.stop_tokens(),
        )

        conversation = [{"role": role, "content": content}]

        chat = self.modelLoader.tokenizer.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
        result = await self.modelLoader.run_single(chat, "0", sampling_params) #userid로 requestid 식별해도 괜찮겠다

        inferResponseDto = InferResponseDto(**{'result': result.outputs[0].text})

        return inferResponseDto

