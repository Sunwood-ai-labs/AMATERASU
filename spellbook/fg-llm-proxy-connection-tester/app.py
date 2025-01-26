import streamlit as st
import openai
import json
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
    try:
        # terraform.tfstateファイルを読み込む
        with open('terraform/terraform.tfstate', 'r') as f:
            tfstate = json.load(f)
        
        # Global Acceleratorのリソースを検索
        for resource in tfstate.get('resources', []):
            if (resource.get('type') == 'aws_globalaccelerator_accelerator' and 
                resource.get('name') == 'main'):
                
                # ip_setsから情報を取得
                ip_sets = resource.get('instances', [])[0].get('attributes', {}).get('ip_sets', [])
                if ip_sets:
                    ip_addresses = ip_sets[0].get('ip_addresses', [])
                    if ip_addresses:
                        return ', '.join(ip_addresses)
                
                # DNSネーム情報も取得
                dns_name = resource.get('instances', [])[0].get('attributes', {}).get('dns_name', '')
                if dns_name:
                    return f"DNS: {dns_name}\nIP: {', '.join(ip_addresses)}"
        
        return "Global Accelerator情報が見つかりません"
    except FileNotFoundError:
        return "terraform.tfstateファイルが見つかりません"
    except Exception as e:
        return f"取得失敗: {str(e)}"
    
def main():
    st.set_page_config(page_title="llm-tester", layout="wide")
    st.title("🚀 llm-tester")

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
