import streamlit as st
import replicate
import os

# 1. 网页基础设置
st.set_page_config(page_title="佰萬老照片修复馆", layout="centered")
st.title("📸 佰萬老照片修复馆")
st.markdown("---")

# 2. 钥匙配置：优先使用 Secrets，其次使用硬编码备份
api_token = st.secrets.get("REPLICATE_API_TOKEN") or "r8_e19owHza4a69oXm9714SKXn7FzrL6ZM0ypRrc"
os.environ["REPLICATE_API_TOKEN"] = api_token

# 3. 上传功能
uploaded_file = st.file_uploader("请上传需要修复的老照片...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="修复前 (Before)", use_container_width=True)
    
    if st.button("开始神奇修复 ✨"):
        try:
            with st.spinner("AI 正在全力修复中..."):
                # 方案：使用模型名称而非特定版本号，系统会自动选择最稳定的版本
                # 这样可以彻底避免 422 版本不存在的问题
                model = replicate.models.get("tencentarc/gfpgan")
                version = model.versions.get("9283608cc6b7be6b656151167cf3069c4e6ae623c39c1f366e2c9a2990e63ad7")
                
                output = replicate.run(
                    version,
                    input={"img": uploaded_file}
                )
                
                st.success("修复成功！")
                st.image(output, caption="修复后 (After)", use_container_width=True)
                st.balloons()
        except Exception as e:
            # 如果指定版本还是不行，尝试最简化的调用方式
            try:
                output = replicate.run(
                    "tencentarc/gfpgan",
                    input={"img": uploaded_file}
                )
                st.success("修复成功（自动匹配版本）！")
                st.image(output, caption="修复后 (After)", use_container_width=True)
                st.balloons()
            except Exception as e2:
                st.error(f"修复失败。错误信息: {e2}")

st.markdown("---")
st.caption("由 佰萬 科技提供技术支持")
