import asyncio
import json
import requests
from fastapi.responses import StreamingResponse

from llama_index.core import Settings
from llama_index.llms.openai_like import OpenAILike

from dto.InferResponse import InferResponse

class InferenceService:

    def __init__(self, modelLoader):
        self.modelLoader = modelLoader

    async def sendInferenceRequest_vLLM(self, role, content):

        conversation = [{"role": role, "content": content}]

        question = self.modelLoader.tokenizer.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)

        response = Settings.llm.complete(question)

        inferResponse = InferResponse(**{'result': str(response)})

        return inferResponse


    async def inference_chatting_streaming(self, messages):

        #embedding해서 rag할 질문은 모든 message를 넣는게 아니라 질문만 정확히 넣어서 찾게 해야될 것 같은데... 수정 필요
        chats = self.modelLoader.tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)

        nodes = self.modelLoader.retriever.retrieve(chats)

        # Generate streaming response
        streaming_response = self.modelLoader.query_engine.synthesize(
            chats,
            nodes=nodes
        )

        def generate():
            for text in streaming_response.response_gen:
                yield text + '\n'

        return generate()