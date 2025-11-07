import time
import streamlit as st

from streamlit.delta_generator import DeltaGenerator

from config import ASSETS_PATH, STORAGE_PATH
from common.utils.image import get_base64_image


def markdown_chatbot_style():
    CHATBOT_STYLE = ASSETS_PATH / 'css' / 'chatbot.css'
    with open(CHATBOT_STYLE) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def markdown_assistant_style():
    PROFILE_BASE64 = get_base64_image(STORAGE_PATH / 'chatbot' / 'profile.png')
    PROFILE_STYLE = f"background-image: url('data:image/png;base64,{PROFILE_BASE64}');" if PROFILE_BASE64 else ""

    st.markdown(f"""
        <style>
        .assistant-profile {{
            width: 26px;
            height: 26px;
            border-radius: 50%;
            {PROFILE_STYLE}
            background-size: cover;
            background-position: center;
            margin-top: 4px;
            flex-shrink: 0;
            box-shadow: 0 0 4px rgba(0,0,0,0.15);
        }}
        </style>
    """, unsafe_allow_html=True)


def init_chatbot_session():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요! 🖐️ Agent 챗봇이에요<br/><br/>궁금하신 점이 있으면 질문을 입력해 주세요 😊"}
        ]


def render_chatbot_container(messages):
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # 기존 메시지 렌더링
    for msg in messages:
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


def render_user_input(prompt: str):
    st.markdown(f"""
        <div class="chat-row user-row">
            <div class="chat-bubble user-bubble">{prompt}</div>
        </div>
    """, unsafe_allow_html=True)


def render_assist_typing_placeholder(typing_placeholder: DeltaGenerator):
    typing_placeholder.markdown(f"""
        <div class="chat-row" style="align-items: center; gap: 8px; margin-top: 6px;">
            <div class="assistant-profile"></div>
            <div class="typing">
                <span></span><span></span><span></span>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_assist_output(message_placeholder: DeltaGenerator, output: str):
    typed_text = ""

    for char in output:
        typed_text += char
        message_placeholder.markdown(f"""
            <div class="chat-row">
                <div class="assistant-profile"></div>
                <div class="chat-bubble assistant-bubble">{typed_text}</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.03)