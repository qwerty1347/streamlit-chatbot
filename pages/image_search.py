import io
import json
from pathlib import Path
import streamlit as st
import requests

from config import STORAGE_PATH
from decouple import config
from PIL import Image

from app.chatbot.components.image_search import markdown_image_search_style
from common.helpers.http_client import http_get


markdown_image_search_style()


class FakeResponse:
    def __init__(self, data):
        self._data = data
        self.status_code = data.get("code", 500)

    def json(self):
        return self._data

st.set_page_config(
    page_title="Image Search",
    page_icon="🖼️",
    layout="centered"
)

st.title("🖼️ Image Search")
st.caption("Upload an image and search via AJAX-style API request")

st.markdown('<div class="upload-box">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "이미지를 업로드하세요",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=False
)
st.markdown('</div>', unsafe_allow_html=True)

# 버튼은 항상 표시
search_clicked = st.button("🔍 Search", use_container_width=True)

# 이미지 미리보기 (업로드 시)
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# 버튼 클릭 로직
if search_clicked:
    # if not uploaded_file:
    #     st.warning("이미지를 먼저 업로드해주세요")
    # else:
    with st.spinner("Searching..."):
        # files = {
        #     "file": (
        #         uploaded_file.name,
        #         uploaded_file.getvalue(),
        #         uploaded_file.type
        #     )
        # }

        try:
            # 유사도 검색 API
            # response = http_get(
            #     url=f"{config('AGENT_API_URL')}/api/v1/agent/image",
            # )


            # ===============================
            # Query Image Section
            # ===============================
            st.markdown("### 🔎 업로드 이미지", unsafe_allow_html=True)

            sample_upload_path = STORAGE_PATH / "image_search" / "apple.jpg"

            if sample_upload_path:
                query_image = Image.open(sample_upload_path)
                st.image(query_image, width=150)
            else:
                st.warning("No uploaded image")

            st.divider()

            sample_json_path = STORAGE_PATH / "image_search" / "sample_images.json"

            with open(sample_json_path, "r", encoding="utf-8") as f:
                sample_json = json.load(f)

            response = FakeResponse(sample_json)

            if response.status_code == 200:
                result = response.json()
                results = result.get("data", [])

                st.success("Search completed")

                # ===============================
                # Similar Images Section
                # ===============================
                st.markdown("### 🖼️ 유사 이미지 결과")

                if not results:
                    st.info("No similar images found")
                    st.stop()

                cols = st.columns(3)

                for idx, item in enumerate(results):
                    col = cols[idx % 3]

                    with col:
                        image_path = item["image_path"]
                        image_url = f"{config('AGENT_API_URL')}{image_path}"

                        st.markdown(
                            f"""
                            <div class="image-box">
                                <img src="{image_url}" />
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                        st.caption(f"Score: {item['score']:.3f}")
                        st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.error(f"Server error: {response.status_code}")

        except Exception as e:
            st.error(f"Request failed: {e}")