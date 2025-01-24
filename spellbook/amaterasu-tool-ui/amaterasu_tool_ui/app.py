"""
Amaterasu Tool UI - GradioベースのWebインターフェース
"""
import gradio as gr
from amaterasu_tool_ui.routes import (
    create_generate_page,
    create_cache_page,
    create_cloudfront_page
)

def create_ui() -> gr.Blocks:
    """
    Gradio UIの作成

    Returns:
        gr.Blocks: Gradioインターフェース
    """
    with gr.Blocks(
        title="Amaterasu Tool UI",
        theme=gr.themes.Soft(
            primary_hue="orange",
            secondary_hue="blue",
        )
    ) as app:
        # ヘッダー
        gr.Markdown("# 🎮 Amaterasu Tool UI")
        gr.Markdown("AWSインフラストラクチャの設定を管理するためのツール")
        
        # タブインターフェース
        with gr.Tabs():
            with gr.TabItem("🔄 Generate TFVars", id=1):
                create_generate_page()
            
            with gr.TabItem("🗑️ Cache Manager", id=2):
                create_cache_page()
            
            with gr.TabItem("🌐 CloudFront TFVars", id=3):
                create_cloudfront_page()
        
        # フッター
        gr.Markdown("---")
        gr.Markdown("""
        📝 [ドキュメント](https://github.com/yourusername/amaterasu-tool)  
        Made with ❤️ by Amaterasu Team
        """)
    
    return app

if __name__ == "__main__":
    app = create_ui()
    app.launch(
        server_name="0.0.0.0",  # すべてのインターフェースでリッスン
        server_port=7860,       # デフォルトポート
        share=False,            # 公開リンクを生成しない
    )
