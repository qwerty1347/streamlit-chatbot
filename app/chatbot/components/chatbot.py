import streamlit as st

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