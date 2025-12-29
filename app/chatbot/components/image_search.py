import streamlit as st

from config import ASSETS_PATH


def markdown_image_search_style():
    IMAGE_SEARCH_STYLE = ASSETS_PATH / 'css' / 'image_search.css'
    with open(IMAGE_SEARCH_STYLE) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
