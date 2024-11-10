import re
from typing import Optional, Dict, List
from bs4 import BeautifulSoup
import markdown
from loguru import logger

class DiffUtils:
    @staticmethod
    def convert_md_to_html(md_content: str) -> str:
        return markdown.markdown(md_content, extensions=['fenced_code', 'codehilite'])

    @staticmethod
    def extract_diff(comment_body: str) -> Optional[Dict[str, str]]:
        logger.info("コメント本文から diff を抽出しています...")
        html_content = DiffUtils.convert_md_to_html(comment_body)
        
        soup = BeautifulSoup(html_content, 'html.parser')
        diff_blocks = soup.find_all('pre', class_='codehilite')
        
        if not diff_blocks:
            logger.error("diff が見つかりません。")
            return None
        
        diffs = {}
        for diff_block in diff_blocks:
            diff_code = diff_block.find('code', class_='language-diff')
            if diff_code:
                diff_content = diff_code.get_text() + "\n"
                file_name = DiffUtils.extract_file_name(diff_content)
                if file_name:
                    diffs[file_name] = diff_content
        
        if not diffs:
            logger.error("有効な diff が見つかりません。")
            return None
        
        logger.info(f"抽出された diff: {len(diffs)} ファイル")
        return diffs

    @staticmethod
    def extract_file_name(diff_content: str) -> Optional[str]:
        file_name_match = re.search(r'^\+\+\+ b/(.+)$', diff_content, re.MULTILINE)
        if file_name_match:
            return file_name_match.group(1)
        return None

    @staticmethod
    def extract_code_block_content(html_content: str) -> str:
        """HTMLコンテンツからコードブロック内の内容を抽出する"""
        soup = BeautifulSoup(html_content, 'html.parser')
        code_block = soup.find('pre', class_='codehilite')
        if code_block:
            code = code_block.find('code')
            if code:
                return code.get_text().strip()
        return ""

def process_diffs(diffs: Dict[str, str], llm_service) -> Dict[str, str]:
    modified_contents = {}
    for file_name, diff in diffs.items():
        with open(file_name, "r", encoding="utf-8") as f:
            original_content = f.read()
        modified_content = llm_service.apply_diff(original_content, diff)
        html_content = DiffUtils.convert_md_to_html(modified_content)
        extracted_content = DiffUtils.extract_code_block_content(html_content)
        modified_contents[file_name] = extracted_content if extracted_content else modified_content
    return modified_contents

def save_files(modified_contents: Dict[str, str]) -> List[str]:
    saved_files = []
    for file_name, content in modified_contents.items():
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"{file_name} に変更を保存しました。")
        saved_files.append(file_name)
    return saved_files

def create_comment(modified_files: List[str], modified_contents: Dict[str, str]) -> str:
    comment = "以下のファイルが変更されました：\n\n"
    for file in modified_files:
        comment += f"- {file}\n\n"
        comment += f"```python\n{modified_contents[file]}\n```\n\n"
    return comment
