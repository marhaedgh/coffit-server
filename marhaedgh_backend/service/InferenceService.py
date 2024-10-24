import asyncio
from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams

class InferenceService:

    def __init__(self, modelLoader):
        self.modelLoader = modelLoader

    def sendInferenceRequest_gRPC(self):

        #gRPC Client ver
        return 0

    def sendInferenceRequest_vLLM(self):
        # vllm serving ver
        sampling_params = SamplingParams(
            temperature=0.0,
            skip_special_tokens=True,
            stop_token_ids=self.modelLoader.stop_tokens(),
        )

        conversation = [{"role": "user", "content": "너가 평가하기에 너는 어느정도의 한국어 실력을 가진 것 같아?"}]
        chat = self.modelLoader.tokenizer.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
        result = asyncio.run(self.modelLoader.run_single(chat, "123"))
        print(result)

        # Runs multiple inferences in parallel
        conversations = [
            [{"role": "user", "content": "세종대왕 맥북 던짐 사건에 대해 말해줘"}],
            [{"role": "user", "content": "2341+12316은 뭐야?"}],
            [{"role": "user", "content": "한국에서 내야하는 세금의 종류에 대해서 알려줘."}],
            [{"role": "user", "content": "개인사업자가 내야하는 특별한 세금이 있을까?"}],
            [{"role": "user", "content": "내가 대회에서 우승할 수 있는 확률을 계산하는 법을 알려줘."}],
        ]
        chats = [
            self.modelLoader.tokenizer.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
            for conversation in conversations
        ]
        results = asyncio.run(self.modelLoader.run_multi(chats))
        print(results)

        return 0


