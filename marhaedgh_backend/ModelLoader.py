import asyncio
from transformers import AutoTokenizer

from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.postprocessor.llm_rerank import LLMRerank
from llama_index.core import get_response_synthesizer
from llama_index.llms.openai_like import OpenAILike

from util.RBLNBGEM3Embeddings import RBLNBGEM3Embeddings


class InferenceModel:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):         # 클래스 객체에 _instance 속성이 없다면
            cls._instance = super().__new__(cls)  # 클래스의 객체를 생성하고 Foo._instance로 바인딩
        return cls._instance 


    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):             # 클래스 객체에 _init 속성이 없다면
            self.llm_llama = OpenAILike(
                model="rbln_vllm_llama-3-Korean-Bllossom-8B_npu8_batch4_max8192",
                api_base="http://0.0.0.0:8000/v1", 
                api_key="1234",
                max_tokens=4096,
                temperature=0.6
            )
            self.llm_prometheus = OpenAILike(
                model="rbln_vllm_prometheus-7b-v2.0_npu2_batch2_max4096",
                api_base="http://0.0.0.0:8001/v1",
                api_key="5678"
            )

            self.embed_model = RBLNBGEM3Embeddings(rbln_compiled_model_name="BGE-m3-ko")
            self.embed_reranker_model = RBLNBGEM3Embeddings(rbln_compiled_model_name="bge-reranker-v2-m3-ko")

            #토크나이저 초기화
            self.tokenizer = AutoTokenizer.from_pretrained("MLP-KTLim/llama-3-Korean-Bllossom-8B")

            # 벡터 스토어 및 인덱스 초기화
            self.vector_store = FaissVectorStore.from_persist_dir("./rag_data")
            self.storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store,
                persist_dir="./rag_data"
            )
            self.index = load_index_from_storage(self.storage_context, embed_model=self.embed_model)
            self.index_rerank = load_index_from_storage(self.storage_context, embed_model=self.embed_reranker_model)

            # Retriever 및 Query Engine 설정
            self.retriever = VectorIndexRetriever(embed_model=self.embed_model, index=self.index, similarity_top_k=2)
            self.retriever_rerank = VectorIndexRetriever(embed_model=self.embed_reranker_model, index=self.index_rerank, similarity_top_k=2)

            self.response_synthesizer = get_response_synthesizer(llm=self.llm_llama, streaming=True, use_async=True)
            self.reranker = LLMRerank(choice_batch_size=5, top_n=3, llm=self.llm_llama)
            self.query_engine = RetrieverQueryEngine(
                retriever=self.retriever,
                response_synthesizer=self.response_synthesizer,
                node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)]
            )

            cls._initialized = True