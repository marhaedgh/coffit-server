import asyncio
from transformers import AutoTokenizer

from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core import get_response_synthesizer

from util.RBLNBGEM3Embeddings import RBLNBGEM3Embeddings


class InferenceModel:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):         # 클래스 객체에 _instance 속성이 없다면
            cls._instance = super().__new__(cls)  # 클래스의 객체를 생성하고 Foo._instance로 바인딩
        return cls._instance 


    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):             # 클래스 객체에 _init 속성이 없다면

            #토크나이저 초기화
            self.tokenizer = AutoTokenizer.from_pretrained("MLP-KTLim/llama-3-Korean-Bllossom-8B")

            # 벡터 스토어 및 인덱스 초기화
            self.vector_store = FaissVectorStore.from_persist_dir("./rag_data")
            self.storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store,
                persist_dir="./rag_data"
            )
            self.index = load_index_from_storage(self.storage_context)

            # Retriever 및 Query Engine 설정
            self.retriever = VectorIndexRetriever(index=self.index, similarity_top_k=2)
            self.response_synthesizer = get_response_synthesizer(streaming=True, use_async=True)
            self.query_engine = RetrieverQueryEngine(
                retriever=self.retriever,
                response_synthesizer=self.response_synthesizer,
                node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)]
            )

            cls._initialized = True


    async def generate_response(self, chat_input):
        sampling_params = SamplingParams(temperature=0.0, max_tokens=1024)
        async for result in self.query_engine.synthesize(chat_input):
            yield result