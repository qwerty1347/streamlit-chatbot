import time
import streamlit as st

from app.chatbot.components.chatbot import init_chatbot_session, markdown_assistant_style, markdown_chatbot_style, render_assist_output, render_assist_typing_placeholder, render_chatbot_container, render_user_input
from app.chatbot.components.sidebar import render_sidebar
from app.chatbot.services.chatbot_service import ChatbotService


st.set_page_config(page_title="chatbot", page_icon="💬", layout="centered")

markdown_chatbot_style()
markdown_assistant_style()
render_sidebar()

chatbot_service = ChatbotService()

# 세션 초기화
init_chatbot_session()

# 채팅 컨테이너 표시
render_chatbot_container(st.session_state.messages)

# 입력창
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 저장 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_user_input(prompt)

    # AI 입력중 표시
    typing_placeholder = st.empty()
    render_assist_typing_placeholder(typing_placeholder)
    time.sleep(1.0)

    # AI 답변 생성
    output = chatbot_service.get_chatbot_output(prompt)
    typing_placeholder.empty()

    # AI 메세지 타이핑 애니메이션 및 표시
    message_placeholder = st.empty()
    render_assist_output(message_placeholder, output)
    st.session_state.messages.append({"role": "assistant", "content": output})
