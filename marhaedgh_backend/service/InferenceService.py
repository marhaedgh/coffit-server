import asyncio
import json
import requests
from fastapi.responses import StreamingResponse

from llama_index.core import QueryBundle

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

        def get_highest_score_text(nodes):

            if not nodes:
                return None

            highest_score_node = max(nodes, key=lambda node: node.score)
            
            return highest_score_node.node.text if hasattr(highest_score_node.node, 'text') else None

        nodes = await self.modelLoader.retriever.aretrieve(question)

        query_bundle = QueryBundle(query_str=question)
        #ranked_nodes = self.retriever_rerank._postprocess_nodes(nodes, query_bundle = query_bundle)

        #final_node = get_highest_score_text(ranked_nodes)
        reranked_nodes = self.modelLoader.reranker.postprocess_nodes(
            nodes, query_bundle
        )

        final_node = get_highest_score_text(reranked_nodes)

        chat = self.modelLoader.tokenizer.apply_chat_template(prompt, add_generation_prompt=True, tokenize=False)

        chat_with_nodes = chat.replace("{nodes}", str(final_node))

        print(chat_with_nodes)
       
        response = await self.modelLoader.llm_llama.astream_complete(chat_with_nodes)

        async for data in response:
            yield data.delta
