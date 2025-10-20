import base64
import time
import streamlit as st

from pathlib import Path

from app.chatbot.services.chatbot_service import ChatbotService


st.set_page_config(page_title="chatbot", page_icon="💬", layout="centered")


def get_base64_image(image_path: str):
    try:

        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        print("이미지 로드 오류:", e)
        return None

PROFILE_IMAGE_PATH = Path("storage/chatbot/profile.png")
PROFILE_BASE64 = get_base64_image(PROFILE_IMAGE_PATH)
PROFILE_STYLE = f"background-image: url('data:image/png;base64,{PROFILE_BASE64}');" if PROFILE_BASE64 else ""


st.markdown("""
    <style>
    .chat-container {
        max-width: 800px;
        margin: auto;
        padding: 20px 0;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .chat-row {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin: 4px 0;
        animation: fadeIn 0.3s ease-in-out;
    }

    .user-row { justify-content: flex-end; }

    .chat-bubble {
        padding: 14px 18px;
        border-radius: 18px;
        max-width: 80%;
        word-wrap: break-word;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        line-height: 1.3;
        transition: all 0.2s ease-in-out;
    }

    .user-bubble {
        background: linear-gradient(135deg, #DCF8C6 0%, #c8f2b5 100%);
        color: #000;
        align-self: flex-end;
    }

    .assistant-bubble {
        background: #f1f0f0;
        color: #111;
        align-self: flex-start;
    }

    .typing {
        font-style: italic;
        color: #888;
        margin-left: 10px;
    }

    .typing span {
        display: inline-block;
        width: 6px;
        height: 6px;
        margin-left: 2px;
        border-radius: 50%;
        background-color: #888;
        animation: blink 1s infinite;
    }

    .typing span:nth-child(1) { animation-delay: 0s; }
    .typing span:nth-child(2) { animation-delay: 0.2s; }
    .typing span:nth-child(3) { animation-delay: 0.4s; }

    @keyframes blink {
        0%, 80%, 100% { opacity: 0; transform: scale(0.5); }
        40% { opacity: 1; transform: scale(1); }
    }

    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(5px);}
        to {opacity: 1; transform: translateY(0);}
    }
    </style>
""", unsafe_allow_html=True)


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
