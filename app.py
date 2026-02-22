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
        st.info("正在连接云端服务器，请稍候...")
        
        # 显示原图
        st.image(uploaded_file, caption="修复前 (Before)", use_column_width=True)
        
        # 4. 调用 AI 修复逻辑
        if st.button("开始神奇修复 ✨"):
            try:
                with st.spinner("AI 正在全力修复中，大约需要 5-10 秒..."):
                    # 调用云端模型
                    output = replicate.run(
                        "tencentarc/gfpgan:0fbacf7afc696e4f97f81385585719902303c0e2124b100752b25b0337604d65",
                        input={"img": uploaded_file}
                    )
                    
                    # 5. 展示修复后的结果
                    st.success("修复成功！")
                    st.image(output, caption="修复后 (After)", use_column_width=True)
                    st.balloons() # 撒花庆祝
            except Exception as e:
                st.error(f"修复失败，请检查网络或 API 余额。错误信息: {e}")

st.markdown("---")
st.caption("由 佰萬 科技提供技术支持 | Vibe Coding 开发")
