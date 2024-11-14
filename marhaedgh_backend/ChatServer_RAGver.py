import requests
import json

from util.RBLNBGEM3Embeddings import RBLNBGEM3Embeddings
from transformers import AutoTokenizer
from sqlalchemy.orm import Session
from llama_index.core import Settings
from llama_index.llms.openai_like import OpenAILike
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.response_synthesizers import TreeSummarize

from db.database import get_db
from repository.NotificationRepository import NotificationRepository

Settings.embed_model = RBLNBGEM3Embeddings()
Settings.llm = OpenAILike(
    model="rbln_vllm_llama-3-Korean-Bllossom-8B_npu4_batch4_max4096",
    api_base="http://0.0.0.0:8000/v1",
    api_key="1234",
    temperature=0.2,
    max_tokens=4096,
    is_chat_model=True
)

tokenizer = AutoTokenizer.from_pretrained("MLP-KTLim/llama-3-Korean-Bllossom-8B")
vector_store = FaissVectorStore.from_persist_dir("./rag_data")
storage_context = StorageContext.from_defaults(
                vector_store=vector_store,
                persist_dir="./rag_data"
            )
index = load_index_from_storage(storage_context)
retriever = VectorIndexRetriever(index=index, similarity_top_k=2)
summarizer = TreeSummarize(llm=Settings.llm)

import streamlit as st

def load_basic_prompt():
    path = "/home/guest/marhaedgh/marhaedgh_backend/prompt/chatting_basic.json"
    with open(path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        return json_data


def add_to_message_history(role, content):
    message = {"role": role, "content": str(content)}
    st.session_state["messages"].append(
        message
    )


with st.chat_message("assistant"):
    st.write("안녕하세요! Coffit AI 에요, 무엇이든 물어보세요! 👋")

notification_summarization = ""
if st.query_params.get("alert_id"):
    db: Session = next(get_db())
    notification_repository = NotificationRepository(db)
    notification = notification_repository.get_notification_by_alert_id(st.query_params["alert_id"])
    notification_summarization = notification.text_summarization

#세션 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        
    ]

if "chat_engine" not in st.session_state:  # Initialize the query engine
    st.session_state["chat_engine"] = index.as_chat_engine(
        chat_mode="context", verbose=True
    )

# 이전 대화 출력 (basic_prompt는 사용자에게 보이지 않음)
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input(
    "궁금한 점을 질문해 주세요!"
):
    add_to_message_history("user", prompt)

    with st.chat_message("user"):
        st.write(prompt)

    basic_prompt = load_basic_prompt()
    retrieved_nodes = retriever.retrieve(prompt)
    added_prompt = basic_prompt["content"].format(question=question, info=notification_summarization, context=retrieved_nodes)

    final_prompt = self.modelLoader.tokenizer.apply_chat_template(added_prompt, add_generation_prompt=False, tokenize=False)
            
    with st.chat_message("assistant"):
        response = st.session_state["chat_engine"].stream_chat(final_prompt)
        response_str = ""
        response_container = st.empty()
        for token in response.response_gen:
            response_str += token
            response_container.markdown(response_str)
        # st.write(response.response)
        add_to_message_history("assistant", response.response)

    # Save the state of the generator
    st.session_state["response_gen"] = response.response_gen