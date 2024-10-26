import asyncio
from transformers import AutoTokenizer
from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams

#vllm 모델 생성 코드

class InferenceModel:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):         # 클래스 객체에 _instance 속성이 없다면
            cls._instance = super().__new__(cls)  # 클래스의 객체를 생성하고 Foo._instance로 바인딩
        return cls._instance 


    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):             # 클래스 객체에 _init 속성이 없다면

            # Please make sure the engine configurations match the parameters used when compiling.
            self.model_id = "MLP-KTLim/llama-3-Korean-Bllossom-8B"
            self.max_seq_len = 4096
            self.batch_size = 4

            self.engine_args = AsyncEngineArgs(
                model=self.model_id,
                device="rbln",
                max_num_seqs=self.batch_size,
                max_num_batched_tokens=self.max_seq_len,
                max_model_len=self.max_seq_len,
                block_size=self.max_seq_len,
                compiled_model_dir="rbln-ko-Llama3-Bllossom-8B",
            )
            self.engine = AsyncLLMEngine.from_engine_args(self.engine_args)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)

            cls._init = True


    def stop_tokens(self):
        eot_id = next((k for k, t in self.tokenizer.added_tokens_decoder.items() if t.content == "<|eot_id|>"), None)
        if eot_id is not None:
            return [self.tokenizer.eos_token_id, eot_id]
        else:
            return [self.tokenizer.eos_token_id]


    # Runs a single inference for an example
    async def run_single(self, chat, request_id, sampling_params):
        results_generator = self.engine.generate(chat, sampling_params, request_id=request_id)
        final_result = None
        async for result in results_generator:
            # You can use the intermediate `result` here, if needed.
            final_result = result
        return final_result


    async def run_multi(self, chats, sampling_params):
        tasks = [asyncio.create_task(self.run_single(chat, i, sampling_params)) for (i, chat) in enumerate(chats)]
        return [await task for task in tasks]

