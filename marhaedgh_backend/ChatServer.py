import streamlit as st
import requests
from sqlalchemy.orm import Session
import json

from db.database import get_db
from repository.NotificationRepository import NotificationRepository

API_URL = "http://localhost:9000/api/v1/infer/chat"

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

# 이전 대화 출력 (basic_prompt는 사용자에게 보이지 않음)
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if question := st.chat_input(
    "궁금한 점을 질문해 주세요!"
):
    add_to_message_history("user", question)
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        
        basic_prompt = load_basic_prompt()
        final_prompt = basic_prompt["content"].format(
            question=question,
            context=notification_summarization,
            messages=st.session_state.messages
        )

        # `st.session_state.messages`를 그대로 사용하여 payload 생성
        payload = {
            "question": question,
            "prompt": [{
                "role": "system",
                "content": final_prompt
            }]
        }

        # 스트리밍 요청 전송
        response = requests.post(
            API_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            stream=True
        )
        
        response_container = st.empty()

        # 서버에서 받은 스트리밍 응답 출력
        full_response = ""
        for chunk in response.iter_content(chunk_size=30):
            if chunk:
                decoded_chunk = chunk.decode("utf-8")
                full_response += decoded_chunk
                response_container.markdown(full_response)
        
        # assistant의 응답을 세션에 추가
        st.session_state.messages.append({"role": "assistant", "content": full_response})
