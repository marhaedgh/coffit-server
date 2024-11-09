import streamlit as st
import requests
from sqlalchemy.orm import Session
import json

from db.database import get_db
from repository.NotificationRepository import NotificationRepository

VLLM_API_URL = "http://localhost:8000/api/v1/chat-infer"

with st.chat_message("user"):
    st.write("Hello 👋")

# 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context_added" not in st.session_state:
    st.session_state.context_added = False

# 알림 ID로 요약문 가져오기
if st.query_params.get("alert_id"):
    db: Session = next(get_db())
    notification_repository = NotificationRepository(db)
    notification = notification_repository.get_notification_by_alert_id(st.query_params["alert_id"])
    main_context = {
        "role": "assistant",
        "content": notification.text_summarization
    }
    
    # 최초 접속 시에만 요약본을 세션에 추가 (사용자에게는 보이지 않음)
    if not st.session_state.context_added:
        st.session_state.messages.insert(0, main_context)
        st.session_state.context_added = True

# 이전 대화 출력 (main_context는 사용자에게 보이지 않음)
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("궁금한 점을 질문해 주세요!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()

        # `st.session_state.messages`를 그대로 사용하여 payload 생성
        payload = {
            "messages": st.session_state.messages,
            "stream": True
        }

        # 스트리밍 요청 전송
        response = requests.post(
            VLLM_API_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            stream=True
        )
        
        # 서버에서 받은 스트리밍 응답 출력
        full_response = ""
        for chunk in response.iter_lines():
            if chunk:
                decoded_chunk = chunk.decode("utf-8")
                full_response += decoded_chunk
                placeholder.markdown(full_response)
        
        # assistant의 응답을 세션에 추가
        st.session_state.messages.append({"role": "assistant", "content": full_response})
