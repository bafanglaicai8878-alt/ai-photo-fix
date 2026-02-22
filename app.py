import streamlit as st
import replicate
import os

# 1. 网页基础设置
st.set_page_config(page_title="佰萬老照片修复馆", layout="centered")
st.title("📸 佰萬老照片修复馆")
st.markdown("---")

# 2. 钥匙配置：强制刷新环境变量，确保支付后的 Token 生效
api_token = st.secrets.get("REPLICATE_API_TOKEN") or "r8_e19owHza4a69oXm9714SKXn7FzrL6ZM0ypRrc"
os.environ["REPLICATE_API_TOKEN"] = api_token

# 3. 上传功能
uploaded_file = st.file_uploader("请上传需要修复的老照片...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # 展示原图
    st.image(uploaded_file, caption="修复前 (Before)", use_container_width=True)
    
    if st.button("开始神奇修复 ✨"):
        try:
            with st.spinner("AI 正在全力修复中，大约需要 5-10 秒..."):
                # 直接调用官方 GFPGAN v1.4 的精确版本，彻底解决 404 和 422 报错
                # 这是目前全网公认最稳定的修复接口
                output = replicate.run(
                    "tencentarc/gfpgan:9283608cc6b7be6b656151167cf3069c4e6ae623c39c1f366e2c9a2990e63ad7",
                    input={
                        "img": uploaded_file,
                        "version": "v1.4",
                        "upscale": 2
                    }
                )
                
                # 展示结果
                st.success("修复成功！")
                st.image(output, caption="修复后 (After)", use_container_width=True)
                st.balloons() # 庆祝动画
                
                # 新增下载按钮，方便客户保存
                st.download_button(
                    label="保存修复后的高清图片",
                    data=output,
                    file_name="fixed_photo.png",
                    mime="image/png"
                )
        except Exception as e:
            st.error(f"修复失败，请稍后再试。错误详情: {e}")

st.markdown
