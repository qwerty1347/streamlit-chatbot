import time
import streamlit as st

from app.chatbot.components.chatbot import markdown_assistant_style, render_chatbot_style
from app.chatbot.services.chatbot_service import ChatbotService


st.set_page_config(page_title="chatbot", page_icon="💬", layout="centered")

render_chatbot_style()
markdown_assistant_style()


chatbot_service = ChatbotService()



# 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 🖐️ Agent 챗봇이에요<br/><br/>궁금하신 점이 있으면 질문을 입력해 주세요 😊"}
    ]

st.sidebar.button("🧹 새 대화", on_click=lambda: st.session_state.clear())

# 채팅 컨테이너 시작
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# 기존 메시지 렌더링
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
            <div class="chat-row user-row">
                <div class="chat-bubble user-bubble">{msg["content"]}</div>
            </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
            <div class="chat-row">
                <div class="assistant-profile"></div>
                <div class="chat-bubble assistant-bubble">{msg["content"]}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 입력창
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 저장 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"""
        <div class="chat-row user-row">
            <div class="chat-bubble user-bubble">{prompt}</div>
        </div>
    """, unsafe_allow_html=True)

    # GPT 입력중 표시
    typing_placeholder = st.empty()
    typing_placeholder.markdown(f"""
        <div class="chat-row" style="align-items: center; gap: 8px; margin-top: 6px;">
            <div class="assistant-profile"></div>
            <div class="typing">
                <span></span><span></span><span></span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1.0)

    # 답변 생성
    reply = chatbot_service.get_chatbot_output(prompt)

    typing_placeholder.empty()

    # 타이핑 애니메이션
    message_placeholder = st.empty()
    typed_text = ""
    for char in reply:
        typed_text += char
        message_placeholder.markdown(f"""
            <div class="chat-row">
                <div class="assistant-profile"></div>
                <div class="chat-bubble assistant-bubble">{typed_text}</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.03)

    st.session_state.messages.append({"role": "assistant", "content": reply})
