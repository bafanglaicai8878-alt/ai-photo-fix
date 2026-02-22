import streamlit as st
import replicate
import os
import requests

# 1. 网页配置
st.set_page_config(page_title="佰萬老照片修复馆", page_icon="📸", layout="centered")

# 自定义 CSS 样式
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #FF4B4B; color: white; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 佰萬老照片修复馆")
st.subheader("用 AI 唤醒尘封的记忆")
st.markdown("---")

# 2. 钥匙配置
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
            with st.spinner("AI 正在全力修复中..."):
                # 锁定官方稳定版本
                output = replicate.run(
                    "tencentarc/gfpgan:9283608cc6b7be6b656151167cf3069c4e6ae623c39c1f366e2c9a2990e63ad7",
                    input={
                        "img": uploaded_file,
                        "upscale": 2,
                        "face_upsample": True,
                        "background_enhance": True
                    }
                )
                
                with col2:
                    st.image(output, caption="修复后 (After)", use_container_width=True)
                
                st.success("✨ 修复成功！")
                st.balloons()
                
                # 下载逻辑
                img_data = requests.get(output).content
                st.download_button(
                    label="📥 保存高清修复图",
                    data=img_data,
                    file_name="fixed_photo.png",
                    mime="image/png"
                )
        except Exception as e:
            st.error(f"❌ 修复失败：{e}")

st.markdown("---")
st.caption("© 2026 佰萬科技 | 技术支持：Vibe Coding")
