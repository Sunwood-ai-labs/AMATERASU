import tempfile
import subprocess
import os
from loguru import logger
import datetime

def create_patch_directory(file_path):
    # ベースとなるパッチディレクトリ
    base_patches_dir = os.path.join(os.getcwd(), 'applied_patches')
    
    # ファイルパスに基づいてサブディレクトリを作成
    relative_dir = os.path.dirname(file_path)
    patches_dir = os.path.join(base_patches_dir, relative_dir)
    
    # ディレクトリが存在しない場合は作成
    os.makedirs(patches_dir, exist_ok=True)
    
    return patches_dir

def apply_patch(patch_file_path, file_path):
    # パッチを保存するディレクトリを作成
    # patches_dir = create_patch_directory(file_path)

    # 現在の日時をファイル名に使用
    # now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # patch_file_name = f"patch_{now}_{os.path.basename(file_path)}.diff"
    # patch_file_path = os.path.join(patches_dir, patch_file_name)

    # print(patch_content)
    
    # パッチをローカルに保存
    # with open(patch_file_path, 'w', encoding='utf-8') as f:
    #     f.write(patch_content)
    logger.info(f"パッチを {patch_file_path} に保存しました。")

    try:
        # パッチを適用
        cmd = ['git', 'apply', patch_file_path, '--ignore-whitespace']
        logger.info("cmd : {}".format(" ".join(cmd)))
        subprocess.run(cmd, check=True)
        logger.info(f"{file_path} にパッチを適用しました。")
        return True
    except subprocess.CalledProcessError:
        logger.error(f"{file_path} へのパッチ適用に失敗しました。")
        return False

def get_patch_file_path(file_path):
    patches_dir = create_patch_directory(file_path)
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    patch_file_name = f"patch_{now}_{os.path.basename(file_path)}.diff"
    return os.path.join(patches_dir, patch_file_name)
