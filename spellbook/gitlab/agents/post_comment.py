import gitlab
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# GitLabクライアントの初期化
gl = gitlab.Gitlab(
    url=os.getenv("GITLAB_URL"),
    private_token=os.getenv("GITLAB_TOKEN")
)

def post_mr_comment(project_id: int, mr_iid: int, comment: str):
    try:
        # プロジェクトとマージリクエストの取得
        project = gl.projects.get(project_id)
        mr = project.mergerequests.get(mr_iid)
        
        # コメントを投稿
        mr.notes.create({'body': comment})
        print("コメントが正常に投稿されました。")
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

# レビューコメントの内容
comment = """## LLMによるマージリクエストレビュー結果

### 評価スコア
|カテゴリ|スコア (1-5)|
|---|:---:|
|コード品質|4|
|セキュリティ|3|
|テスト|1|
|アーキテクチャ|3|
|総合評価|3|

### コード品質
**長所:**
- コードの構造が明確で理解しやすい
- 適切な変数名とコメントが使用されている
- エラーハンドリングが実装されている

**短所:**
- 重複コードが存在する（add_comment copy.py と add_comment copy 2.py）
- 定数の定義がグローバルスコープにある

### セキュリティ評価
⚠️ 環境変数からの機密情報の取得方法が適切だが、値の存在チェックがない
⚠️ APIトークンがコード内に直接記述されている

### 改善提案
1. 重複ファイルを削除し、一つのスクリプトに統合する
2. 環境変数の存在チェックを追加する
3. APIリクエスト部分を関数化して再利用性を高める
4. テストコードを追加する
5. エラーメッセージをより詳細にする
6. コンフィグファイルを使用して設定を外部化する

### 総評
コードは基本的な機能を果たしており、理解しやすい構造になっています。しかし、重複ファイルの存在、テストの欠如、セキュリティ面での改善の余地があります。関数化やエラーハンドリングの強化、テストの追加、そして設定の外部化を行うことで、コードの品質と保守性を大幅に向上させることができるでしょう。また、セキュリティ面での注意点にも対処することが重要です。"""

if __name__ == "__main__":
    post_mr_comment(9, 1, comment)