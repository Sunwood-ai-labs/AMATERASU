"""
UIスタイルの定義を提供するモジュール
"""
import os

def get_style_definitions():
    """
    スタイル定義を取得

    Returns:
        str: スタイル定義のCSS
    """
    try:
        css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'styles.css')
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        return f"<style>{css_content}</style>"
    except Exception as e:
        print(f"スタイルシートの読み込みに失敗しました: {str(e)}")
        return "<style></style>"
