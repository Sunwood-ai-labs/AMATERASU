#!/usr/bin/env python3
"""
ラベル分類機能のテストスクリプト
"""
import sys
import os
import csv

# Add the parent directory of 'scripts' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from services.llm_service import LLMService

def load_labels_from_csv(csv_path):
    labels = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            labels.append(row['label'])
    return labels

def test_label_classification():
    logger.info("ラベル分類機能のテストを開始します")
    
    # ラベルリストの読み込み
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'labels.csv')
    existing_labels = load_labels_from_csv(csv_path)
    logger.info(f"読み込まれたラベル: {', '.join(existing_labels)}")
    
    # テストケースの定義
    test_cases = [
        {
            "title": "📝 [docs] リリース後のREADME自動更新 (v0.5.0)",
            "body": "このプルリクエストは、リリース v0.5.0 に基づいてREADMEを自動更新したものです。",
            "is_pr": True,
            "expected_labels": ["documentation", "automated pr"]
        },
        {
            "title": "✨ Supabaseプロファイル管理機能の実装",
            "body": "Supabaseにプロファイル管理機能を実装し、関連するドキュメントを更新",
            "is_pr": False,
            "expected_labels": ["enhancement", "feature"]
        },
        {
            "title": "🐛 ログイン時のエラーを修正",
            "body": "認証プロセスで発生していたバグを修正しました。",
            "is_pr": False,
            "expected_labels": ["bug"]
        },
        {
            "title": "♻️ LiteLLM設定ファイルの構成改善",
            "body": "設定ファイル構成の改善とDockerコンテナ設定の最適化",
            "is_pr": False,
            "expected_labels": ["enhancement"]
        }
    ]
    
    # テストの実行
    llm_service = LLMService()
    
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"\n=== テストケース {i} ===")
        logger.info(f"タイトル: {test_case['title']}")
        logger.info(f"Pull Request: {test_case['is_pr']}")
        logger.info(f"期待されるラベル: {', '.join(test_case['expected_labels'])}")
        
        try:
            # LLMによる分析
            suggested_labels = llm_service.analyze_issue(
                test_case['title'],
                test_case['body'],
                existing_labels,
                test_case['is_pr']
            )
            
            label_list = [label.strip().replace("*", "") for label in suggested_labels.split(',')]
            
            # 自動PRの検出ロジックをシミュレート
            if test_case['is_pr'] and 'docs' in test_case['title'].lower():
                if 'automated pr' not in label_list:
                    label_list.append('automated pr')
                    logger.info("自動PRを検出し、'automated pr'ラベルを追加")
            
            logger.info(f"提案されたラベル: {', '.join(label_list)}")
            
            # 結果の検証
            expected_set = set(test_case['expected_labels'])
            suggested_set = set(label_list)
            
            if expected_set.issubset(suggested_set):
                logger.success("✅ テスト成功: 期待されるラベルがすべて含まれています")
            else:
                missing = expected_set - suggested_set
                logger.warning(f"⚠️ 一部のラベルが欠けています: {', '.join(missing)}")
                
        except Exception as e:
            logger.error(f"❌ テスト中にエラーが発生しました: {str(e)}")
    
    logger.info("\n=== テスト完了 ===")

if __name__ == "__main__":
    test_label_classification()
