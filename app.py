import streamlit as st
import replicate
import os
import requests

# 1. 网页配置
st.set_page_config(page_title="佰萬老照片修复馆", page_icon="📸", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #FF4B4B; color: white; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 佰萬老照片修复馆")
st.subheader("用新动力唤醒老记忆")
st.markdown("---")

# 2. 令牌配置：强制刷新环境变量
api_token = st.secrets.get("REPLICATE_API_TOKEN")

if not api_token:
    st.error("⚠️ 令牌未识别！请在 Secrets 中配置新的 REPLICATE_API_TOKEN。")
    st.stop()
else:
    os.environ["REPLICATE_API_TOKEN"] = api_token

# 3. 业务功能区
uploaded_file = st.file_uploader("第一步：上传老照片...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    col1, col2 = st.columns(2)
    with col1:
        st.image(uploaded_file, caption="修复前", use_container_width=True)
    
    if st.button("第二步：开始神奇修复 ✨"):
        try:
            with st.spinner("新令牌已就绪，正在精准连接 AI 模型..."):
                # --- 解决 404 的关键：使用完整路径 + 精确版本号 ---
                # 这种写法是 Replicate 官方最推荐的，不会找错房间
                model_id = "tencentarc/gfpgan:9283608cc6b7be6b656151167cf3069c4e6ae623c39c1f366e2c9a2990e63ad7"
                
                output = replicate.run(
                    model_id,
                    input={
                        "img": uploaded_file,
                        "upscale": 2,
                        "face_upsample": True,
                        "background_enhance": True
                    }
                )
                
                if output:
                    with col2:
                        st.image(output, caption="修复后", use_container_width=True)
                    st.success("✨ 修复成功！")
                    st.balloons()
                    
                    # 下载功能
                    img_data = requests.get(output).content
                    st.download_button(
                        label="📥 点击保存高清图",
                        data=img_data,
                        file_name="fixed_photo.png",
                        mime="image/png"
                    )
        except Exception as e:
            st.error(f"❌ 修复遇到了点小问题：{e}")

st.markdown("---")
st.caption("© 2026 佰萬科技 | 令牌与路径已重校")
