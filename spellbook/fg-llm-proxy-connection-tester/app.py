import streamlit as st
import openai
import json
import os
import socket
import dns.resolver
import requests
import os

def get_ip_info():
    # パブリックIPの取得
    try:
        public_ip = requests.get('https://api.ipify.org').text
    except:
        public_ip = "取得失敗"
    
    # ローカルIPの取得
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "取得失敗"
        
    return {
        "パブリックIP": public_ip,
        "ローカルIP": local_ip,
        "ホスト名": hostname
    }

def get_global_accelerator_ip():
    dns_name = os.environ.get('GLOBAL_ACCELERATOR_DNS_NAME')
    if dns_name:
        resolver = dns.resolver.Resolver()
        try:
            ip_addresses = [str(ip.address) for ip in resolver.resolve(dns_name, 'A')]
            ip_address_str = ", ".join(ip_addresses)
            return f"DNS: {dns_name}\nIPアドレス: {ip_address_str}"
        except Exception as e:
            print(f"DNS resolution failed: {e}")
            return f"取得失敗: {str(e)}"
    return "Global Accelerator DNS名が設定されていません"
    
def main():
    st.set_page_config(page_title="llm-tester", layout="wide")
    st.title("🚀 llm-tester v0.1")

    # サイドバーに設定項目を配置
    with st.sidebar:
        st.header("🛠️ 設定")
        base_url = st.text_input("LiteLLM Proxy URL", "http://0.0.0.0:4000")
        api_key = st.text_input("API Key", "your_api_key", type="password")
        model = st.text_input("モデル名", "gpt-4o-mini")
        max_tokens = st.number_input("最大トークン数", min_value=1, value=1000)
        temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
        
        # デバッグ情報の表示
        st.header("🔍 デバッグ情報")
        ip_info = get_ip_info()
        for key, value in ip_info.items():
            st.text(f"{key}: {value}")

        # グローバルアクセラレータのIPアドレスを表示
        st.header("🌐 グローバルアクセラレータ情報")
        global_accelerator_ip = get_global_accelerator_ip()
        st.text(f"IPアドレス: {global_accelerator_ip}")

    # メインエリアにプロンプト入力と結果表示
    prompt = st.text_area("プロンプトを入力してください", height=200)
    
    if st.button("送信"):
        if not prompt:
            st.warning("プロンプトを入力してください")
            return
            
        try:
            with st.spinner("処理中..."):
                # OpenAI clientの設定
                client = openai.OpenAI(
                    api_key=api_key,
                    base_url=base_url
                )
                
                # リクエストの実行
                response = client.chat.completions.create(
                    model=model,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                # 結果の表示
                st.subheader("🤖 応答")
                st.markdown(response.choices[0].message.content)
                
                # デバッグ用にレスポンス全体を表示
                with st.expander("🔍 デバッグ: レスポンス全体"):
                    st.code(json.dumps(response.model_dump(), indent=2, ensure_ascii=False), language="json")

        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()
