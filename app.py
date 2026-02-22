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

# 2. 钥匙配置：确保 API Token 正确加载
api_token = st.secrets.get("REPLICATE_API_TOKEN")

if not api_token:
    st.error("⚠️ 还没找到‘钥匙’！请在 Streamlit 后台的 Secrets 中配置 REPLICATE_API_TOKEN。")
    st.stop()
else:
    # 强制注入环境变量，这是解决权限问题的关键
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
                # --- 修改重点：使用动态获取模型的方式，彻底避开 422 版本不存在的问题 ---
                # 直接调用模型路径而不带后缀乱码，Replicate 会自动匹配你账号权限下最稳的版本
                model_path = "tencentarc/gfpgan"
                
                output = replicate.run(
                    model_path,
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
            # 增加更友好的中文报错提示
            if "422" in str(e):
                st.error("❌ 修复失败（错误 422）：模型版本权限调整，请尝试重新部署应用。")
            elif "402" in str(e) or "payment" in str(e).lower():
                st.error("❌ 余额不足或支付未生效，请检查 Replicate 账单详情。")
            else:
                st.error(f"❌ 修复失败：{e}")

st.markdown("---")
st.caption("© 2026 佰萬科技 | 技术支持：Vibe Coding")
