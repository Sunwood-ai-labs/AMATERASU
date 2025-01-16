"""
ページ設定とヘッダー関連のUIコンポーネントを提供するモジュール
"""
import streamlit as st

def set_page_config():
    """ページの初期設定を行う"""
    st.set_page_config(
        page_title="Terraform Vars Generator",
        page_icon="🎮",
        layout="wide"
    )
    
    # モダンなテーマカラーを設定
    st.markdown("""
        <style>
        :root {
            --bg-light: #FAF6EA;    /* 明るいベージュ */
            --bg-medium: #DBD3BE;    /* ミディアムベージュ */
            --accent-light: #C99F75; /* キャメル */
            --accent-dark: #906B65;  /* ブラウン */
            --text-color: #463F44;   /* ダークグレー */
            --font: 'Inter', system-ui, -apple-system, sans-serif;
        }
        
        /* 全体の背景色とグラデーション */
        .stApp {
            background: linear-gradient(135deg, var(--bg-light), var(--bg-medium)) !important;
        }
        
        /* ヘッダーのスタイル */
        h1 {
            color: var(--text-color) !important;
            font-family: var(--font) !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
            text-shadow: 2px 2px 4px rgba(70,63,68,0.1);
        }
        
        h2, h3 {
            font-family: var(--font) !important;
            color: var(--text-color) !important;
            font-weight: 600 !important;
        }
        
        /* フォームコントロールのスタイル */
        .stTextInput > div > div > input {
            background: linear-gradient(to right, var(--bg-light), var(--bg-medium));
            border-radius: 8px;
            border: 1px solid var(--accent-light);
            padding: 8px 12px;
            color: var(--text-color);
            font-weight: 500;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--accent-dark);
            box-shadow: 0 0 0 2px rgba(144,107,101,0.2);
        }
        
        .stSelectbox > div > div > select {
            background: linear-gradient(to right, var(--bg-light), var(--bg-medium));
            border-radius: 8px;
            border: 1px solid var(--accent-light);
            padding: 8px 12px;
            color: var(--text-color);
            font-weight: 500;
        }
        
        /* ボタンのスタイル */
        .stButton > button {
            background: linear-gradient(135deg, var(--accent-light) 0%, var(--accent-dark) 100%) !important;
            color: var(--bg-light) !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 0.6rem 1.2rem !important;
            font-family: var(--font) !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 2px 4px rgba(144,107,101,0.2);
            text-shadow: 1px 1px 1px rgba(70,63,68,0.2);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, var(--accent-dark) 0%, var(--accent-light) 100%) !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(144,107,101,0.3) !important;
        }
        
        /* エクスパンダーのスタイル */
        .streamlit-expanderHeader {
            background: linear-gradient(to right, var(--bg-light), var(--bg-medium)) !important;
            border-radius: 8px !important;
            border: 1px solid var(--accent-light) !important;
            color: var(--text-color) !important;
            transition: all 0.3s ease;
            backdrop-filter: blur(8px);
            font-weight: 500;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: var(--accent-dark) !important;
            background: linear-gradient(to right, var(--bg-medium), var(--bg-light)) !important;
        }
        
        /* プログレスバーのスタイル */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, var(--accent-light), var(--accent-dark)) !important;
        }
        
        /* エラーメッセージのスタイル */
        .stAlert > div {
            border-radius: 8px !important;
            background: linear-gradient(to right, rgba(144,107,101,0.05), rgba(201,159,117,0.05)) !important;
            border-left: 4px solid var(--accent-dark) !important;
            backdrop-filter: blur(8px);
        }
        
        /* コードブロックのスタイル */
        .stMarkdown code {
            background: linear-gradient(45deg, var(--bg-medium), var(--bg-light));
            padding: 2px 6px;
            border-radius: 4px;
            color: var(--text-color);
            border: 1px solid var(--accent-light);
            font-weight: 500;
        }
        
        /* リンクのスタイル */
        .stMarkdown a {
            color: var(--accent-dark) !important;
            text-decoration: none;
            background: linear-gradient(to bottom, 
                transparent 0%, 
                transparent 60%, 
                rgba(144,107,101,0.2) 60%, 
                rgba(144,107,101,0.2) 100%
            );
            transition: all 0.3s ease;
            padding: 0 2px;
        }
        
        .stMarkdown a:hover {
            color: var(--accent-light) !important;
            background: linear-gradient(to bottom, 
                transparent 0%, 
                transparent 60%, 
                rgba(201,159,117,0.3) 60%, 
                rgba(201,159,117,0.3) 100%
            );
        }

        /* その他のテキストスタイル */
        .element-container {
            color: var(--text-color);
            font-weight: 500;
        }
        
        /* カスタムスクロールバー */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--bg-medium);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(var(--accent-light), var(--accent-dark));
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(var(--accent-dark), var(--accent-light));
        }
        </style>
    """, unsafe_allow_html=True)

def show_header():
    """ヘッダーを表示"""
    st.title("🎮 Terraform Variables Generator")
    st.markdown("""
    ### 概要
    このツールは、`terraform/main-infrastructure`ディレクトリを持つ
    プロジェクトに対して、`terraform.tfvars`ファイルを自動生成します。
    
    以下の共通設定を一括で生成できます：
    - 🔒 セキュリティグループID
    - 🌐 サブネットID
    - 🏢 VPC設定
    - 🔍 Route53ゾーン情報
    """)

def initialize_page():
    """ページの初期化を行う"""
    set_page_config()
    show_header()
