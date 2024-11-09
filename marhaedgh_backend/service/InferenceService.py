import asyncio
from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams

from dto.InferResponse import InferResponse

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

        inferResponse = InferResponse(**{'result': result.outputs[0].text})

        return inferResponse


    async def inference_chatting_streaming(self, messages):
        sampling_params = SamplingParams(
            temperature=0.0,
            skip_special_tokens=True,
            stop_token_ids=self.modelLoader.stop_tokens(),
        )

        # 이전 출력된 텍스트 길이를 추적
        previous_length = 0

        chats = self.modelLoader.tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)

        async for result in self.modelLoader.engine.generate(chats, sampling_params, request_id="chat0"):
            # 현재 생성된 전체 텍스트 가져오기
            current_text = result.outputs[0].text
            
            # 새로운 텍스트 부분만 추출
            new_text = current_text[previous_length:]
            previous_length = len(current_text)

            # 새로운 부분만 출력
            if new_text.strip():  # 새로운 텍스트가 존재하면 출력
                yield new_text + "\n"
