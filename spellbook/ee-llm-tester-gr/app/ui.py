"""UI関連のコンポーネントとレイアウト"""

import gradio as gr
from typing import Tuple
from app.models import MODEL_PRESETS, load_preset
from app.utils import get_ip_info

def create_ui(process_prompt_fn) -> gr.Blocks:
    """Gradio UIの作成"""
    with gr.Blocks(title="LLM Tester", theme=gr.themes.Ocean()) as interface:
        gr.Markdown("# 🚀 LLM Tester v0.2")
        
        with gr.Row():
            with gr.Column(scale=2):
                # メインのプロンプト入力エリア
                prompt_input = gr.TextArea(
                    label="📝 プロンプトを入力",
                    placeholder="テストしたいプロンプトをここに入力してください...",
                    lines=10
                )
                
                with gr.Row():
                    submit_btn = gr.Button("🚀 送信", variant="primary")
                    clear_btn = gr.Button("🗑️ クリア", variant="secondary")
                
                response_output = gr.Markdown(label="応答")
                debug_output = gr.Markdown(label="デバッグ情報")
                
            with gr.Column(scale=1):
                with gr.Tab("モデル設定"):
                    preset_dropdown = gr.Dropdown(
                        choices=list(MODEL_PRESETS.keys()),
                        value="GPT-3.5 Turbo",
                        label="モデルプリセット"
                    )
                    model = gr.Textbox(
                        label="モデル名",
                        value="gpt-3.5-turbo",
                        placeholder="使用するモデル名"
                    )
                    max_tokens = gr.Number(
                        label="最大トークン数",
                        value=1000,
                        minimum=1,
                        maximum=4000
                    )
                    temperature = gr.Slider(
                        label="Temperature",
                        minimum=0.0,
                        maximum=2.0,
                        value=1.0,
                        step=0.1
                    )

                with gr.Tab("接続設定"):
                    base_url = gr.Textbox(
                        label="LiteLLM Proxy URL",
                        value="http://0.0.0.0:4000",
                        placeholder="例: http://0.0.0.0:4000"
                    )
                    api_key = gr.Textbox(
                        label="API Key",
                        value="your_api_key",
                        type="password",
                        placeholder="OpenAI API キーを入力"
                    )

                with gr.Tab("システム情報"):
                    ip_info = get_ip_info()
                    gr.Markdown("\n".join([
                        f"**{k}**: {v}" for k, v in ip_info.items()
                    ]))
                
                with gr.Tab("ヘルプ"):
                    gr.Markdown("""
                        ### 使い方
                        1. プリセットを選択するか、詳細設定を行います
                        2. プロンプトを入力します
                        3. 送信ボタンをクリックして結果を確認します
                        
                        ### トラブルシューティング
                        - API エラーの場合は API Key を確認してください
                        - 接続エラーの場合は Proxy URL を確認してください
                        - レスポンスが遅い場合は max_tokens を調整してください
                    """)
        
        def clear_outputs() -> Tuple[str, str]:
            return ["", ""]
        
        # イベントハンドラの設定
        preset_dropdown.change(
            fn=load_preset,
            inputs=[preset_dropdown],
            outputs=[model, max_tokens, temperature]
        )
        
        submit_btn.click(
            fn=process_prompt_fn,
            inputs=[
                prompt_input,
                base_url,
                api_key,
                model,
                max_tokens,
                temperature
            ],
            outputs=[
                response_output,
                debug_output
            ]
        )
        
        clear_btn.click(
            fn=clear_outputs,
            inputs=[],
            outputs=[response_output, debug_output]
        )
    
    return interface
