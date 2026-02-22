import streamlit as st
import replicate
import os

# 1. 网页基础设置
st.set_page_config(page_title="佰萬老照片修复馆", layout="centered")
st.title("📸 佰萬老照片修复馆")
st.markdown("---")

# 2. 检查钥匙是否配置成功
api_token = st.secrets.get("REPLICATE_API_TOKEN") or os.environ.get("REPLICATE_API_TOKEN")

if not api_token:
    st.error("⚠️ 还没找到‘钥匙’ (API Token)！请在 Streamlit 后台的 Secrets 中配置。")
else:
    # 3. 上传功能
    uploaded_file = st.file_uploader("请上传需要修复的老照片...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # 显示原图
        st.image(uploaded_file, caption="修复前 (Before)", use_container_width=True)
        
        # 4. 调用 AI 修复逻辑
        if st.button("开始神奇修复 ✨"):
            try:
                # 显式设置环境变量，确保 replicate 库能读取到钥匙
                os.environ["REPLICATE_API_TOKEN"] = api_token
                
                with st.spinner("AI 正在全力修复中，大约需要 5-10 秒..."):
                    # 使用当前最稳定的 GFPGAN 版本号
                    # 修复了之前导致 422 错误的旧版本地址
                    output = replicate.run(
                        "tencentarc/gfpgan:9283608cc6b7be6b656151167cf3069c4e6ae623c39c1f366e2c9a2990e63ad7",
                        input={
                            "img": uploaded_file,
                            "version": "v1.4",
                            "upscale": 2
                        }
                    )
                    
                    # 5. 展示修复后的结果
                    st.success("修复成功！")
                    st.image(output, caption="修复后 (After)", use_container_width=True)
                    st.balloons() # 撒花庆祝
                    
                    # 提供下载按钮
                    st.download_button(
                        label="保存高清修复图",
                        data=output,
                        file_name="fixed_photo.png",
                        mime="image/png"
                    )
            except Exception as e:
                st.error(f"修复失败，请检查网络或 API 余额。错误信息: {e}")

st.markdown("---")
st.caption("由 佰萬 科技提供技术支持 | Vibe Coding 开发")
