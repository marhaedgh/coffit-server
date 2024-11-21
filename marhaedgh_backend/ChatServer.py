import streamlit as st
import requests
from sqlalchemy.orm import Session
import json
import time

from db.database import get_db
from repository.NotificationRepository import NotificationRepository

API_URL = "http://localhost:9000/api/v1/infer/chat"

def load_basic_prompt():
    path = "/home/guest/marhaedgh/marhaedgh_backend/prompt/chatting.json"
    with open(path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        return json_data

def add_to_message_history(role, content):
    st.session_state["messages"].append({"role": role, "content": content})

# 메시지 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "summarization_loaded" not in st.session_state:
    st.session_state["summarization_loaded"] = False  # 요약 메시지 출력 여부 플래그

notification_summarization = ""
if st.query_params.get("alert_id") and not st.session_state["summarization_loaded"]:
    db: Session = next(get_db())
    notification_repository = NotificationRepository(db)
    notification = notification_repository.get_notification_by_alert_id(st.query_params["alert_id"])
    notification_summarization = notification.text_summarization

    # 요약 데이터를 대화 메시지로 추가
    summarized_lines = notification_summarization.split("\n")
    for line in summarized_lines:
        if line.strip():
            add_to_message_history("assistant", line.strip())
    st.session_state["summarization_loaded"] = True

# **이전 메시지 출력**
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # 최초 notification summarization 메시지에만 2초 딜레이 추가
        if not st.session_state.get("summarization_displayed", False):
            time.sleep(2)

st.session_state["summarization_displayed"] = True  # 딜레이는 요약 메시지에만 한 번 적용

# 사용자 입력 처리
if question := st.chat_input("궁금한 점을 질문해 주세요!"):
    # 사용자 질문 추가
    add_to_message_history("user", question)
    with st.chat_message("user"):
        st.markdown(question)

    # AI 응답 처리
    with st.chat_message("assistant"):
        basic_prompt = load_basic_prompt()
        final_prompt = basic_prompt["content"].format(
            question=question,
            nodes="{nodes}",
            messages=json.dumps(st.session_state["messages"], ensure_ascii=False)
        )

        payload = {
            "question": question,
            "prompt": [{
                "role": "system",
                "content": final_prompt
            }]
        }
        print(final_prompt)
        response = requests.post(
            API_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            stream=True
        )

        response_container = st.empty()
        full_response = ""
        for chunk in response.iter_content(chunk_size=30):
            if chunk:
                decoded_chunk = chunk.decode("utf-8")
                full_response += decoded_chunk
                response_container.markdown(full_response)

        # AI 응답 추가
        add_to_message_history("assistant", full_response)
