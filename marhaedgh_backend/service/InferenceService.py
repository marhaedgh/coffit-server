import asyncio
import json
import requests
from fastapi.responses import StreamingResponse

from dto.InferResponse import InferResponse

class InferenceService:

    def __init__(self, modelLoader):
        self.modelLoader = modelLoader


    async def sendInferenceRequest_vLLM(self, role, content):
       
        conversation = [{"role": role, "content": content}]

        question = self.modelLoader.tokenizer.apply_chat_template(conversation, add_generation_prompt=True, tokenize=True)
        
        response = await self.modelLoader.llm_llama.acomplete(question)

        inferResponse = InferResponse(**{'result': str(response)})

        return inferResponse
    
    
    async def inference_chatting_streaming(self, question, prompt):

        nodes = await self.modelLoader.retriever.aretrieve(question)

        def get_highest_score_text(nodes):

            if not nodes:
                return None

            highest_score_node = max(nodes, key=lambda node: node.score)
            
            return highest_score_node.node.text if hasattr(highest_score_node.node, 'text') else None
        
        final_node = get_highest_score_text(nodes)

        chat = self.modelLoader.tokenizer.apply_chat_template(prompt, add_generation_prompt=True, tokenize=False)

        chat_with_nodes = chat.replace("{nodes}", str(final_node))

        print(chat_with_nodes)
       
        response = await self.modelLoader.llm_llama.astream_complete(chat_with_nodes)

        async for data in response:
            yield data.delta
