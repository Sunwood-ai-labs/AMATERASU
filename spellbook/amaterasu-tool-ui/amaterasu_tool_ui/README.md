# 🎮 Amaterasu Tool UI

AWSインフラストラクチャ設定管理ツールのGradioベースWebインターフェース

## 🌟 特徴

- 🔍 プロジェクトの視覚的な探索
- 🚀 直感的なterraform.tfvars生成
- 🧹 キャッシュ管理の簡素化
- 📊 リッチなプロジェクト情報の表示

## 📦 インストール

```bash
# 依存関係のインストール
pip install -r requirements.txt
```

## 🚀 使用方法

### アプリケーションの起動

```bash
python app.py
```

アプリケーションが起動すると、デフォルトでhttp://localhost:7860 でアクセスできます。

### 基本的な操作フロー

1. プロジェクトの探索
   - ベースディレクトリを指定
   - 必要に応じてCloudFrontオプションを選択
   - 「プロジェクトをスキャン」をクリック

2. プロジェクトの設定
   - プラットフォームの名称を入力
   - 対象プロジェクトを選択
   - 「設定ファイル生成」をクリック

3. キャッシュ管理
   - 対象プロジェクトを選択
   - 「キャッシュ削除」をクリック

## 🖥️ スクリーンショット

### プロジェクト探索
![Project Discovery](./assets/discovery.png)

### 設定生成
![Settings Generation](./assets/generation.png)

### キャッシュ管理
![Cache Management](./assets/cache.png)

## 🛠️ カスタマイズ

### ポート番号の変更

```python
app.launch(server_port=8080)  # app.pyの最後の行を変更
```

### テーマのカスタマイズ

```python
with gr.Blocks(
    title="Amaterasu Tool UI",
    theme=gr.themes.Soft()  # または他のテーマを選択
) as app:
    # ...
```

## 📝 依存パッケージ

- gradio>=4.0.0
- amaterasu-tool==0.1.0
- python-dotenv>=1.0.0
- rich>=13.0.0

## ⚙️ 開発

### 開発環境のセットアップ

```bash
# 仮想環境の作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt
```

### コードフォーマット

```bash
# black（フォーマッター）
black app.py
```

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. フィーチャーブランチを作成（`git checkout -b feature/amazing-feature`）
3. 変更をコミット（`git commit -m '✨ Add some amazing feature'`）
4. ブランチにプッシュ（`git push origin feature/amazing-feature`）
5. プルリクエストを作成

## ⚠️ 注意事項

- base-infrastructure/output.jsonが存在しない場合、デフォルト値が使用されます
- キャッシュ削除の操作は取り消せません
- 設定を変更する前に、必ずバックアップを作成してください

## 📄 ライセンス

MITライセンスで提供されています。
