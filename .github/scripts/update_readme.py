import os
import sys

# Add the parent directory of 'scripts' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from github import Github
from loguru import logger
from config import get_settings
from services.llm_service import LLMService

def main():
    logger.info("README更新プロセスを開始します。")
    
    settings = get_settings()
    llm_service = LLMService()
    g = Github(settings.YOUR_PERSONAL_ACCESS_TOKEN_IRIS)
    repo = g.get_repo(settings.GITHUB_REPOSITORY)

    # 最新のリリースを取得
    latest_release = repo.get_latest_release()
    logger.info(f"最新のリリース: {latest_release.title}")

    # READMEの内容を取得
    readme = repo.get_contents("README.md")
    readme_content = readme.decoded_content.decode("utf-8")
    
    repo_summary_path = ".SourceSageAssets/DOCUMIND/Repository_summary.md"
    repo_summary_content = ""

    # リポジトリのサマリーファイルをローカルから読み込む
    try:
        with open(repo_summary_path, 'r', encoding='utf-8') as f:
            repo_summary_content = f.read()
        logger.info("リポジトリのサマリーファイルを読み込みました。")
    except FileNotFoundError:
        logger.warning(f"リポジトリのサマリーファイルが見つかりません: {repo_summary_path}")
    except Exception as e:
        logger.warning(f"リポジトリのサマリーファイルの読み込みに失敗しました: {str(e)}")

    # LLMにプロンプトを送信

    prompt = f"""
以下の情報を元に、READMEを更新してください：

# 更新のガイドライン:
<Update guidelines>
1. リポジトリの目的、主要機能、使用方法、インストール手順など、ユーザーにとって重要な情報を簡潔に記載してください。
2. 最新のリリースで追加された主要な機能や重要な変更点のみをREADME内の適切な位置に簡潔に記載してください。詳細な更新情報は不要です。
3. 既存のマークダウンやHTMLの構造を維持しつつ、必要な箇所のみを更新してください。
4. リポジトリのサマリーを参考にして、プロジェクトの概要が正確に伝わるようにしてください。
5. 読みやすく、理解しやすい日本語で記述してください。
6. 最新のバージョン番号を記載してください。
7. 各主要セクションの見出しに適切な絵文字を追加してください。以下は提案する絵文字の例です：
   - プロジェクト概要: 🚀
   - 主な機能: ✨
   - 使用方法: 🔧
   - インストール手順: 📦
   - 最新情報: 🆕
   - ライセンス: 📄
8. 絵文字は適度に使用し、読みやすさを損なわないようにしてください。
9. リポジトリ中身を深く観察し存在しないファイルへのパスは記載しないで
10. READMEの上にリリースノートを付けるような形式ではなく、READMEの中身の各章を更新する形式で更新してください。
11. > [!IMPORTANT] などの注釈部分には手を加えないでそのままにして

更新されたREADMEの全文をそのまま出力してください。
</Update guidelines>

# 最新のリリース情報:
<Latest release information>
バージョン: {latest_release.title}
主な変更点:
{latest_release.body}
</Latest release information>

# リポジトリのサマリー:
<Repository summary>
{repo_summary_content}
</Repository summary>



    """

    logger.info("LLMに更新を依頼しています...")
    logger.info(f"プロンプト：\n{prompt}")
    updated_readme = llm_service.get_response(prompt, remove_code_block=True)

    logger.info(f">> updated_readme：\n{updated_readme}")
    
    # 更新されたREADMEの内容をファイルに書き込む
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_readme)

    logger.info("READMEの更新が完了しました。")

if __name__ == "__main__":
    main()
