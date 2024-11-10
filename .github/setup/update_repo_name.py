import os
import sys
from loguru import logger

def update_files(new_repo_name):
    logger.info(f"リポジトリ名を '{new_repo_name}' に更新します")

    files_to_update = [
        '.github/workflows/publish-to-pypi.yml',
        '.github/workflows/sync-to-huggingface.yml',
        '.github/release_notes/.sourcesage_releasenotes_iris.yml'
    ]

    for file_path in files_to_update:
        full_path = os.path.join(os.getcwd(), file_path)
        if not os.path.exists(full_path):
            logger.warning(f"ファイル {full_path} が見つかりません。スキップします。")
            continue

        logger.info(f"{file_path} の処理を開始します")

        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read()

        updated_content = content.replace('HarmonAI_III', new_repo_name)

        if content != updated_content:
            with open(full_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            logger.success(f"{file_path} を更新しました")
        else:
            logger.info(f"{file_path} には変更が必要ありませんでした")

if __name__ == "__main__":

    if len(sys.argv) != 2:
        logger.error("使用方法: python update_repo_name.py <新しいリポジトリ名>")
        sys.exit(1)

    new_repo_name = sys.argv[1]
    logger.info(f"スクリプトを開始します。新しいリポジトリ名: {new_repo_name}")

    try:
        update_files(new_repo_name)
        logger.success("リポジトリ名の更新が完了しました")
    except Exception as e:
        logger.exception(f"更新処理中にエラーが発生しました: {str(e)}")
        sys.exit(1)

# ---------------------------
# コマンドメモ
#
# python .github\setup\update_repo_name.py x-archive-visualizer
