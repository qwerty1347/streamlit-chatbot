import streamlit as st


def render_sidebar():
    st.sidebar.button("🧹 새 대화", on_click=lambda: st.session_state.clear())