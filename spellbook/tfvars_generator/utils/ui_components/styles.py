"""
UIスタイルの定義を提供するモジュール
"""

def get_style_definitions():
    """
    スタイル定義を取得

    Returns:
        str: スタイル定義のCSS
    """
    return """
    <style>
    :root {
        --bg-light: #F5F5F5;    /* 明るい背景 */
        --bg-medium: #E5E5E5;    /* やや暗い背景 */
        --text-dark: #363432;    /* チャコールグレー */
        --accent1: #196774;      /* ティールブルー */
        --accent2: #90A19D;      /* セージグレー */
        --accent3: #F0941F;      /* オレンジ */
        --font: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* 全体の背景色とグラデーション */
    .stApp {
        background: linear-gradient(135deg, var(--bg-light), var(--bg-medium)) !important;
        color: var(--text-dark);
    }
    
    /* ヘッダーのスタイル */
    h1 {
        color: var(--text-dark) !important;
        font-family: var(--font) !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        text-shadow: 1px 1px 2px rgba(54,52,50,0.1);
    }
    
    h2, h3, h4 {
        font-family: var(--font) !important;
        color: var(--text-dark) !important;
        font-weight: 600 !important;
    }
    
    /* フォームコントロールのスタイル */
    .stTextInput > div > div > input {
        background: var(--bg-light);
        border-radius: 8px;
        border: 1px solid var(--accent2);
        padding: 8px 12px;
        color: var(--text-dark);
        font-weight: 500;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent1);
        box-shadow: 0 0 0 2px rgba(25,103,116,0.1);
    }
    
    .stSelectbox > div > div > select {
        background: var(--bg-light);
        border-radius: 8px;
        border: 1px solid var(--accent2);
        padding: 8px 12px;
        color: var(--text-dark);
        font-weight: 500;
    }
    
    /* ボタンのスタイル */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent1), var(--accent2)) !important;
        color: var(--bg-light) !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.6rem 1.2rem !important;
        font-family: var(--font) !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 4px rgba(25,103,116,0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--accent2), var(--accent1)) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(25,103,116,0.3) !important;
    }
    
    /* エクスパンダーのスタイル */
    .streamlit-expanderHeader {
        background: var(--bg-light) !important;
        border-radius: 8px !important;
        border: 1px solid var(--accent2) !important;
        color: var(--text-dark) !important;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: var(--accent1) !important;
        background: var(--bg-medium) !important;
    }
    
    /* プログレスバーのスタイル */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent1), var(--accent2)) !important;
    }
    
    /* エラーメッセージのスタイル */
    .stAlert > div {
        border-radius: 8px !important;
        background: var(--bg-light) !important;
        border-left: 4px solid var(--accent3) !important;
        color: var(--text-dark);
    }
    
    /* コードブロックのスタイル */
    .stMarkdown code {
        background: var(--bg-medium);
        padding: 2px 6px;
        border-radius: 4px;
        color: var(--text-dark);
        border: 1px solid var(--accent2);
        font-weight: 500;
    }
    
    /* リンクのスタイル */
    .stMarkdown a {
        color: var(--accent1) !important;
        text-decoration: none;
        background: linear-gradient(to bottom,
            transparent 0%,
            transparent 60%,
            rgba(25,103,116,0.1) 60%,
            rgba(25,103,116,0.1) 100%
        );
        transition: all 0.3s ease;
        padding: 0 2px;
    }
    
    .stMarkdown a:hover {
        color: var(--accent3) !important;
        background: linear-gradient(to bottom,
            transparent 0%,
            transparent 60%,
            rgba(240,148,31,0.1) 60%,
            rgba(240,148,31,0.1) 100%
        );
    }

    /* その他のテキストスタイル */
    .element-container {
        color: var(--text-dark);
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
        background: linear-gradient(var(--accent2), var(--accent1));
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(var(--accent1), var(--accent2));
    }
    </style>
    """
