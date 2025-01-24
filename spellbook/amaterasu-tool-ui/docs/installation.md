# 🚀 インストールガイド

## 前提条件

- Python 3.9以上
- uvicorn[standard]
- uv (高速なPythonパッケージマネージャー)

## 🔧 環境構築

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/amaterasu-tool-ui.git
cd amaterasu-tool-ui
```

### 2. 仮想環境の作成と有効化

```bash
python -m venv .venv
source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
```

### 3. 依存パッケージのインストール

uvを使用してパッケージをインストールします：

```bash
uv pip install -r requirements.txt
```

### 4. amaterasu-toolパッケージのインストール

開発モードでamaterasu-toolをインストールします：

```bash
uv pip install -e .
```

### 5. 確認

インストールが正常に完了したことを確認します：

```bash
python -c "import amaterasu_tool; print(amaterasu_tool.__version__)"
```

バージョン番号（例：0.1.0）が表示されれば成功です。

## 🔍 トラブルシューティング

### ImportError: attempted relative import beyond top-level package

このエラーが発生した場合は、以下のように環境変数`PYTHONPATH`を設定してください：

```bash
export PYTHONPATH=/path/to/amaterasu-tool-ui:$PYTHONPATH
```

または実行時に直接指定：

```bash
PYTHONPATH=/path/to/amaterasu-tool-ui python amaterasu_tool_ui/app.py
```

### その他の問題

- パッケージのインストールに失敗する場合は、pipを最新版にアップデートしてみてください：
  ```bash
  uv pip install --upgrade pip
  ```

- 依存関係の競合が発生する場合は、仮想環境を作り直してください：
  ```bash
  deactivate
  rm -rf .venv
  python -m venv .venv
  source .venv/bin/activate
