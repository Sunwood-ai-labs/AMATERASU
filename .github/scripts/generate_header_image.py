import os
import sys

# Add the parent directory of 'scripts' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_settings
from services.image_service import ImageService
from loguru import logger

def create_release_headers(tag: str, output_dir: str, font_name: str):
    logger.info(f"ヘッダー画像の生成を開始: タグ '{tag}', フォント '{font_name}', 出力先 '{output_dir}'")
    image_service = ImageService()

    # タグ付きの画像を生成
    tagged_output_path = os.path.join(output_dir, f"release_header_{tag}.png")
    image_service.generate_header_image(tag, tagged_output_path, font_name, use_smooth_area=True, target_ratio=0.8)
    logger.success(f"タグ付きヘッダー画像を生成しました: {tagged_output_path}")

    # 最新版の画像を生成
    latest_output_path = os.path.join(output_dir, "release_header_latest.png")
    image_service.generate_header_image(tag, latest_output_path, font_name, use_smooth_area=True, target_ratio=0.8)
    logger.success(f"最新版ヘッダー画像を生成しました: {latest_output_path}")

if __name__ == "__main__":
   
    logger.info("画像生成スクリプトを開始します。")
    
    settings = get_settings()
    tag = os.environ.get('LATEST_TAG', 'v1.0.0')
    font_name = ".github/release_notes/fonts/HigherJump-8MZ7M.ttf"
    logger.info(f"使用するタグ: {tag}")
    logger.info(f"使用するフォント: {font_name}")
    
    output_dir = os.path.join(settings.RELEASE_NOTES_DIR, "header_image").replace(".github", "docs")
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"出力ディレクトリ: {output_dir}")
    
    create_release_headers(tag, output_dir, font_name)
    
    logger.info("画像生成スクリプトが正常に終了しました。")
