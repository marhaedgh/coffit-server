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
        
        response = await Settings.llm.acomplete(question)

        inferResponse = InferResponse(**{'result': str(response)})

        return inferResponse
    
    
    async def inference_chatting_streaming(self, question, prompt):

        nodes = self.modelLoader.retriever.retrieve(question)
        #print(nodes)

        chat = self.modelLoader.tokenizer.apply_chat_template(prompt, add_generation_prompt=True, tokenize=False)

        # Generate streaming response
        streaming_response = self.modelLoader.query_engine.synthesize(
            chat,
            nodes=nodes
        )
        
        def generator():
            for text in streaming_response.response_gen:
                #print(text)
                yield text

        return generator()