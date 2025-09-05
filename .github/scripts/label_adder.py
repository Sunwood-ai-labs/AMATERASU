import sys
import os
import csv

# Add the parent directory of 'scripts' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from config import get_settings
from services.llm_service import LLMService
from services.github_service import GitHubService

def load_labels_from_csv(csv_path):
    labels = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            labels.append(row['label'])
    return labels

def main():
    logger.info("イシューの処理を開始します。")
    
    settings = get_settings()
    llm_service = LLMService()
    github_service = GitHubService()

    logger.info("GitHubからイシューを取得しています...")
    issue = github_service.get_issue()
    logger.info(f"イシュー #{issue.number} を取得しました: {issue.title}")

    logger.info("labels.csvからラベルのリストを読み込んでいます...")
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'labels.csv')
    existing_labels = load_labels_from_csv(csv_path)
    logger.info(f"読み込まれたラベル: {', '.join(existing_labels)}")
    
    # Pull Requestかどうかを確認
    is_pr = hasattr(issue, 'pull_request') and issue.pull_request is not None
    
    logger.info("LLMを使用してイシューを分析し、ラベルを提案しています...")
    suggested_labels = llm_service.analyze_issue(issue.title, issue.body, existing_labels, is_pr)
    
    label_list = [label.strip().replace("*", "") for label in suggested_labels.split(',')]
    
    # 自動PRの検出とラベル追加
    if is_pr and ('iris-s-coon' in str(issue.user.login) or 'bot' in str(issue.user.login).lower()):
        if 'automated pr' not in label_list:
            label_list.append('automated pr')
            logger.info("自動生成されたPRを検出し、'automated pr'ラベルを追加しました")
    
    logger.info(f"提案されたラベル: {', '.join(label_list)}")

    # 提案されたラベルを検証し、未登録のラベルをスキップ
    validated_labels = []
    skipped_labels = []
    for label in label_list:
        if label in existing_labels:
            validated_labels.append(label)
        else:
            skipped_labels.append(label)

    logger.info(f"検証済みのラベル: {', '.join(validated_labels)}")
    if skipped_labels:
        logger.warning(f"未登録のためスキップされたラベル: {', '.join(skipped_labels)}")

    logger.info("検証済みのラベルをイシューに適用しています...")
    github_service.add_labels(issue, validated_labels)

    logger.info("イシューにコメントを追加しています...")
    comment = f"I.R.I.S Bot🤖が以下のラベルを提案し、適用しました：\n\n" + "\n".join([f"- {label}" for label in validated_labels])
    if skipped_labels:
        comment += f"\n\n以下のラベルは未登録のためスキップされました：\n\n" + "\n".join([f"- {label}" for label in skipped_labels])
    github_service.add_comment(issue, comment)

    logger.info("イシューの処理が完了しました。")

if __name__ == "__main__":
    main()
