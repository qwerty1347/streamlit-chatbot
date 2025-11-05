import streamlit as st

from config import STORAGE_PATH
from common.utils.image import get_base64_image


def render_chatbot_style():
    st.markdown("""
        <style>
            .chat-container {
                max-width: 800px;
                margin: auto;
                padding: 8px 0 20px 0;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }

            .chat-row {
                display: flex;
                align-items: flex-start;
                gap: 12px;
                margin-bottom: 10px;
                animation: fadeIn 0.3s ease-in-out;
            }

            .user-row { justify-content: flex-end; }

            .chat-bubble {
                padding: 14px 18px;
                border-radius: 18px;
                width: fit-content;
                max-width: 480px;
                word-wrap: break-word;
                white-space: pre-wrap;
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