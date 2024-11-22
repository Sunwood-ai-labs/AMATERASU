# main.py
import streamlit as st
from utils import generate_prompt, HEADER_HTML

st.set_page_config(layout="wide")

def main():
    st.markdown(HEADER_HTML, unsafe_allow_html=True)

    task_or_prompt = st.text_area("タスクの説明または既存のプロンプトを入力してください：")

    if st.button("プロンプトを生成"):
        if task_or_prompt:
            with st.spinner("プロンプトを生成中..."):
                generated_prompt = generate_prompt(task_or_prompt)
                st.subheader("生成されたプロンプト：")
                st.markdown(generated_prompt)
        else:
            st.warning("タスクの説明または既存のプロンプトを入力してください。")

if __name__ == "__main__":
    main()
