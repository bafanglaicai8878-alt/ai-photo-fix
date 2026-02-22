import streamlit as st
import replicate
import os
import requests

# 1. 网页配置：设置标题和布局
st.set_page_config(page_title="佰萬老照片修复馆", page_icon="📸", layout="centered")

# 自定义 CSS 样式，美化按钮和文字
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #FF4B4B; color: white; height: 3em; }
    .main { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 佰萬老照片修复馆")
st.subheader("用 AI 唤醒尘封的记忆")
st.markdown("---")

# 2. 钥匙配置：强制从 Secrets 读取
api_token = st.secrets.get("REPLICATE_API_TOKEN")

if not api_token:
    st.error("⚠️ 还没找到‘钥匙’！请在 Streamlit 后台的 Secrets 中配置 REPLICATE_API_TOKEN。")
    st.stop()
else:
    os.environ["REPLICATE_API_TOKEN"] = api_token

# 3. 业务功能区
uploaded_file = st.file_uploader("请上传需要修复的老照片...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    col1, col2 = st.columns(2)
    with col1:
        st.image(uploaded_file, caption="修复前 (Before)", use_container_width=True)
    
    if st.button("开始神奇修复 ✨"):
        try:
            with st.spinner("AI 正在全力修复中，大约需要 5-10 秒..."):
                # 使用官方最稳定的 GFPGAN v1.4 版本，彻底解决 422 报错
                output = replicate.run(
                    "tencentarc/gfpgan:9283608cc6b7be6b656151167cf3069c4e6ae623c39c1f366e2c9a2990e63ad7",
                    input={
                        "img": uploaded_file,
                        "upscale": 2,
                        "face_upsample": True,
                        "background_enhance": True
                    }
                )
                
                with
