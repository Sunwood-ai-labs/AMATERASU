# 👨‍💻 開発者ガイド

## 🏗️ プロジェクト構造

```plaintext
amaterasu-tool-ui/
├── amaterasu_tool/          # コアライブラリパッケージ
│   ├── config/             # 設定管理
│   ├── tests/             # テストスイート
│   └── utils/             # ユーティリティ関数
├── amaterasu_tool_ui/      # Web UIパッケージ
│   ├── components/        # UIコンポーネント
│   ├── routes/           # ページルーティング
│   └── utils/            # UI用ユーティリティ
└── docs/                   # ドキュメント
```

## 🔧 開発環境のセットアップ

### 依存関係のインストール（開発用）

```bash
# poetryを使用する場合
poetry install

# uvを使用する場合
uv pip install -r requirements.txt -r requirements-dev.txt
```

### 開発用サーバーの起動

```bash
# デバッグモードで起動
PYTHONPATH=/path/to/amaterasu-tool-ui python amaterasu_tool_ui/app.py
```

## 🧪 テスト

### テストの実行

```bash
# すべてのテストを実行
pytest

# カバレッジレポートの生成
pytest --cov=amaterasu_tool

# 特定のテストファイルを実行
pytest amaterasu_tool/tests/test_config.py
```

### テストの作成

新しい機能を追加する場合は、対応するテストも作成してください：

```python
# test_example.py
def test_new_feature():
    # テストのセットアップ
    result = some_function()
    # アサーション
    assert result == expected_value
```

## 🔍 コード品質

### リンターとフォーマッター

```bash
# コードフォーマット
black .

# 型チェック
mypy .

# リンター
flake8
```

### コーディング規約

- PEP 8に従う
- 型ヒントを使用
- docstringは日本語で記述
- コメントは必要最小限に

## 🔄 開発ワークフロー

1. 新機能の開発
   ```bash
   git checkout -b feature/新機能名
   ```

2. テストの作成と実行
   ```bash
   pytest
   ```

3. コードフォーマットとリント
   ```bash
   black .
   flake8
   mypy .
   ```

4. コミット
   ```bash
   git commit -m "✨ 新機能: 機能の説明"
   ```

## 📝 コミットメッセージの規約

```
<絵文字> <タイプ> #<Issue番号>: <タイトル>
<本文>
<フッター>
```

### タイプ一覧

- feat: 新機能
- fix: バグ修正
- docs: ドキュメントの変更
- style: コードスタイルの変更
- refactor: リファクタリング
- perf: パフォーマンス改善
- test: テストの追加・修正
- chore: ビルドプロセスやツールの変更

## 🔍 デバッグ

### デバッグモードの有効化

```python
import debugpy

# デバッグポートを開く
debugpy.listen(("0.0.0.0", 5678))
```

### ログの設定

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 📚 API ドキュメント

各モジュールのAPIドキュメントは、docstringから自動生成されます。

- コアライブラリ: `amaterasu_tool.__init__.py`
- UIコンポーネント: `amaterasu_tool_ui.components.__init__.py`
- ルート: `amaterasu_tool_ui.routes.__init__.py`

## ⚠️ 既知の問題

1. TerraformProjectオブジェクトのシリアライズ
2. 相対インポートの問題
3. PYTHONPATHの設定が必要

## 🔜 今後の改善点

1. コンポーネントのリファクタリング
2. エラーハンドリングの改善
3. ロギング機能の強化
4. テストカバレッジの向上
