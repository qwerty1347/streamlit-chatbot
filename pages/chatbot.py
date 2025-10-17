import streamlit as st
import time

from datetime import datetime


st.set_page_config(page_title="chatbot", page_icon="💬", layout="centered")

st.markdown("""
    <style>
    .chat-container {
        max-width: 800px;
        margin: auto;
        padding: 20px 0;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }

    .chat-row {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin: 6px 0;
        animation: fadeIn 0.3s ease-in-out;
    }

    /* AI 프로필 */
    .assistant-profile {
        width: 26px;
        height: 26px;
        border-radius: 50%;
        background: linear-gradient(135deg, #7BA8FF, #4E6CFF);
        margin-top: 4px;
        flex-shrink: 0;
        box-shadow: 0 0 4px rgba(0,0,0,0.15);
    }

    /* 사용자 말풍선 */
    .user-row { justify-content: flex-end; }

    .chat-bubble {
        padding: 12px 16px;
        border-radius: 16px;
        max-width: 80%;
        word-wrap: break-word;
        position: relative;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1);
        line-height: 1.5;
        transition: all 0.2s ease-in-out;
    }

    .user-bubble {
        background: linear-gradient(135deg, #DCF8C6 0%, #c8f2b5 100%);
        color: #000;
        align-self: flex-end;
        border-bottom-right-radius: 4px;
    }

    .assistant-bubble {
        background: #f1f0f0;
        color: #111;
        align-self: flex-start;
        border-bottom-left-radius: 4px;
    }

    .assistant-bubble::before {
        content: "";
        position: absolute;
        bottom: 0;
        left: -6px;
        width: 0;
        height: 0;
        border-right: 10px solid #f1f0f0;
        border-top: 8px solid transparent;
        border-bottom: 8px solid transparent;
    }

    /* 타이핑 애니메이션 */
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






import requests

def get_gpt_response(user_input: str) -> str:
    """
    API 호출해서 GPT 응답 받아오기
    """

    print(user_input)

    API_URL = "/api/v1/agent/chatbot"  # 실제 API 주소
    try:
        response = requests.get(API_URL, params={"query": user_input}, timeout=10)
        if response.status_code == 200:

            data = response.json()
            st.write("API Response:", data)

            print(data)
            return data.get("reply", "죄송합니다. 답변을 받지 못했습니다 😅")

        else:
            print("ERROR")
            return f"API 오류: {response.status_code}"

    except Exception as e:
        return f"API 호출 실패: {str(e)}"








# 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 😊 저는 GPT 챗봇이에요.\n무엇을 도와드릴까요?"}
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
            <div class="assistant-profile" style="width: 24px; height: 24px; margin-top: 2px;"></div>
            <div class="typing">
                <span></span><span></span><span></span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1.0)

    # 답변 생성
    reply = get_gpt_response(prompt)

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
