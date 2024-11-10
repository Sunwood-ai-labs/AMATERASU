import os
import sys

# Add the parent directory of 'scripts' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Tuple, Optional, List
import random
from PIL import Image, ImageDraw, ImageFont

from config import get_settings
from services.color_analyzer import ColorAnalyzer

from loguru import logger
import matplotlib.font_manager
import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans



class ImageService:
    def __init__(self):
        self.settings = get_settings()
        self.font_cache = {}
        # ColorAnalyzerのインスタンスを作成
        self.color_analyzer = ColorAnalyzer(pixel_skip=4)
    
    def get_random_background(self):
        logger.info("ランダムな背景画像を選択中...")
        background_dir = os.path.join(self.settings.RELEASE_NOTES_DIR, 'assets')
        background_images = [f for f in os.listdir(background_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        if not background_images:
            logger.error("背景画像が見つかりません。")
            raise FileNotFoundError("No background images found in the assets directory.")
        selected_image = random.choice(background_images)
        logger.success(f"背景画像 '{selected_image}' を選択しました。")
        return os.path.join(background_dir, selected_image)
    
    def list_available_fonts(self):
        logger.info("使用可能なフォントの一覧を表示します...")
        
        # システムフォントの一覧
        system_fonts = set(f.name for f in matplotlib.font_manager.fontManager.ttflist)
        logger.info("システムフォント:")
        for font in sorted(system_fonts):
            logger.info(f"  - {font}")
        
        # カスタムフォント
        custom_font_dir = os.path.join(self.settings.RELEASE_NOTES_DIR, 'assets')
        custom_fonts = [f for f in os.listdir(custom_font_dir) if f.endswith('.ttf')]
        if custom_fonts:
            logger.info("カスタムフォント:")
            for font in custom_fonts:
                logger.info(f"  - {font}")
        else:
            logger.info("カスタムフォントは見つかりませんでした。")
    
    def get_font(self, font_name, font_size):
        # logger.info(f"フォント '{font_name}' (サイズ: {font_size}) を読み込み中...")
        
        if (font_name, font_size) in self.font_cache:
            return self.font_cache[(font_name, font_size)]
        
        # 指定されたフォントファイルを探す
        if os.path.exists(font_name):
            try:
                font = ImageFont.truetype(font_name, font_size)
                # logger.success(f"指定されたフォントファイル '{font_name}' を読み込みました。")
                self.font_cache[(font_name, font_size)] = font
                return font
            except OSError:
                logger.warning(f"指定されたフォントファイル '{font_name}' の読み込みに失敗しました。")
        
        # assets ディレクトリ内でフォントを探す
        font_extensions = ['.otf', '.ttf']
        for ext in font_extensions:
            custom_font_path = os.path.join(self.settings.RELEASE_NOTES_DIR, 'assets', font_name + ext)
            if os.path.exists(custom_font_path):
                try:
                    font = ImageFont.truetype(custom_font_path, font_size)
                    logger.success(f"カスタムフォント '{custom_font_path}' を読み込みました。")
                    self.font_cache[(font_name, font_size)] = font
                    return font
                except OSError:
                    logger.warning(f"カスタムフォント '{custom_font_path}' の読み込みに失敗しました。")
        
        # システムフォントを探す
        try:
            font_path = matplotlib.font_manager.findfont(matplotlib.font_manager.FontProperties(family=font_name))
            font = ImageFont.truetype(font_path, font_size)
            logger.success(f"システムフォント '{font_name}' を読み込みました。")
            self.font_cache[(font_name, font_size)] = font
            return font
        except OSError:
            logger.warning(f"システムフォント '{font_name}' の読み込みに失敗しました。")
        
        # フォールバック: デフォルトフォント
        logger.warning(f"フォント '{font_name}' が見つかりませんでした。デフォルトフォントを使用します。")
        default_font = ImageFont.load_default().font_variant(size=font_size)
        self.font_cache[(font_name, font_size)] = default_font
        return default_font
    
    def calculate_optimal_font_size(self, rect_width, rect_height, text, font_name, target_ratio=0.9):
        font_size = 1
        while True:
            font = self.get_font(font_name, font_size)
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            if text_width > rect_width * target_ratio or text_height > rect_height * target_ratio:
                return font_size - 1
            
            font_size += 1

    def detect_smooth_areas(self, image, kernel_size=5, threshold=10):
        img_array = np.array(image.convert('L'))
        kernel = np.ones((kernel_size, kernel_size)) / (kernel_size ** 2)
        convolved = convolve2d(img_array, kernel, mode='same', boundary='symm')
        diff = np.abs(img_array - convolved)
        smooth_areas = diff < threshold
        return smooth_areas, diff

    def visualize_smooth_areas(self, image, smooth_areas, diff, output_dir):
        # オリジナル画像
        plt.figure(figsize=(10, 10))
        plt.imshow(image)
        plt.title("Original Image")
        plt.axis('off')
        plt.savefig(os.path.join(output_dir, "original_image.png"))
        plt.close()

        # 差分のヒートマップ
        plt.figure(figsize=(10, 10))
        plt.imshow(diff, cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.title("Difference Heatmap")
        plt.axis('off')
        plt.savefig(os.path.join(output_dir, "difference_heatmap.png"))
        plt.close()

        # 滑らかな領域のマスク
        plt.figure(figsize=(10, 10))
        plt.imshow(smooth_areas, cmap='binary')
        plt.title("Smooth Areas Mask")
        plt.axis('off')
        plt.savefig(os.path.join(output_dir, "smooth_areas_mask.png"))
        plt.close()

    def find_largest_rectangle(self, binary_image):
        h, w = binary_image.shape
        heights = np.zeros((h, w), dtype=int)

        for i in range(h):
            for j in range(w):
                if binary_image[i][j]:
                    heights[i][j] = heights[i-1][j] + 1 if i > 0 else 1

        max_area = 0
        max_rect = (0, 0, 0, 0)

        for i in range(h):
            stack = []
            for j in range(w + 1):
                if j < w:
                    height = heights[i][j]
                else:
                    height = 0

                start = j
                while stack and stack[-1][1] > height:
                    top = stack.pop()
                    area = (j - top[0]) * top[1]
                    if area > max_area:
                        max_area = area
                        max_rect = (top[0], i - top[1] + 1, j - 1, i)
                    start = top[0]
                stack.append((start, height))

        return max_rect

    def detect_smooth_areas(self, image, kernel_size=5, threshold=10):
        img_array = np.array(image.convert('L'))
        kernel = np.ones((kernel_size, kernel_size)) / (kernel_size ** 2)
        convolved = convolve2d(img_array, kernel, mode='same', boundary='symm')
        diff = np.abs(img_array - convolved)
        smooth_areas = diff < threshold
        return smooth_areas, diff

    def visualize_smooth_areas(self, image, smooth_areas, diff, output_dir):
        # オリジナル画像
        plt.figure(figsize=(10, 10))
        plt.imshow(image)
        plt.title("Original Image")
        plt.axis('off')
        plt.savefig(os.path.join(output_dir, "original_image.png"))
        plt.close()

        # 差分のヒートマップ
        plt.figure(figsize=(10, 10))
        plt.imshow(diff, cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.title("Difference Heatmap")
        plt.axis('off')
        plt.savefig(os.path.join(output_dir, "difference_heatmap.png"))
        plt.close()

        # 滑らかな領域のマスク
        plt.figure(figsize=(10, 10))
        plt.imshow(smooth_areas, cmap='binary')
        plt.title("Smooth Areas Mask")
        plt.axis('off')
        plt.savefig(os.path.join(output_dir, "smooth_areas_mask.png"))
        plt.close()

    def visualize_largest_rectangle(self, image, rect, output_path):
        draw = ImageDraw.Draw(image)
        draw.rectangle(rect, outline="red", width=3)
        image.save(output_path)

    def calculate_contrast(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
        """
        Calculate the contrast ratio between two colors.
        """
        def luminance(color):
            r, g, b = [x / 255.0 for x in color[:3]]
            return 0.2126 * r + 0.7152 * g + 0.0722 * b

        l1 = luminance(color1)
        l2 = luminance(color2)
        return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

    def find_highest_contrast_color(self, background_color: Tuple[int, int, int], palette: List[List[int]]) -> Tuple[int, int, int]:
        """
        Find the color from the palette with the highest contrast to the background color.
        """
        max_contrast = 0
        best_color = None
        for color in palette:
            contrast = self.calculate_contrast(background_color, tuple(color))
            if contrast > max_contrast:
                max_contrast = contrast
                best_color = color
        return tuple(best_color)

    def get_dominant_color_in_rect(self, img: Image.Image, rect: Tuple[int, int, int, int]) -> Tuple[int, int, int]:
        """
        Get the dominant color in the specified rectangle of the image.
        """
        cropped_img = img.crop(rect)
        colors = cropped_img.getcolors(cropped_img.width * cropped_img.height)
        sorted_colors = sorted(colors, key=lambda x: x[0], reverse=True)
        return sorted_colors[0][1]

    def generate_header_image(self, tag: str, output_path: str, font_name: str = "Times New Roman", 
                              use_smooth_area: bool = False, target_ratio: float = 0.5, 
                              text_color: Optional[Tuple[int, int, int]] = None):
        logger.info(f"ヘッダー画像の生成を開始: タグ '{tag}', フォント '{font_name}', 余白検出 {'有効' if use_smooth_area else '無効'}")
        background_path = self.get_random_background()
        
        logger.info("背景画像を開いています...")
        img = Image.open(background_path)
        
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # ColorAnalyzerを使用してカラーパレットを抽出
        logger.info("画像全体からカラーパレットを抽出しています...")
        palette = self.color_analyzer.extract_color_palette_quadrants(img, n_colors=40)
        
        draw = ImageDraw.Draw(img)
        
        if use_smooth_area:
            logger.info("余白領域を検出中...")
            smooth_areas, diff = self.detect_smooth_areas(img)
            self.visualize_smooth_areas(img, smooth_areas, diff, output_dir)
            
            rect = self.find_largest_rectangle(smooth_areas)
            logger.info(f"検出された最大の余白領域: {rect}")
            self.visualize_largest_rectangle(img.copy(), rect, os.path.join(output_dir, "largest_rectangle.png"))
        else:
            rect = (0, 0, img.width, img.height)
            logger.info(f"従来の手法: 画像全体を使用 {rect}")
        
        rect_width = rect[2] - rect[0]
        rect_height = rect[3] - rect[1]
        font_size = self.calculate_optimal_font_size(rect_width, rect_height, tag, font_name, target_ratio)
        
        logger.info(f"最適化されたフォントサイズ: {font_size}")
        font = self.get_font(font_name, font_size)
        
        bbox = font.getbbox(tag)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # テキストを余白の中央に配置
        x = rect[0] + (rect_width - text_width) // 2
        y = rect[1] + (rect_height - text_height) // 2
        position = (x, y)
        
        # テキスト色の決定
        margin_dominant_color = self.get_dominant_color_in_rect(img, rect)
        if text_color is None:
            text_color = self.find_highest_contrast_color(margin_dominant_color[:3], palette)  # RGBのみを使用
            logger.info(f"余白の支配的な色: {margin_dominant_color[:3]}")  # RGBのみをログに記録
            logger.info(f"選択されたテキスト色: {text_color}")
            contrast_ratio = self.calculate_contrast(margin_dominant_color[:3], text_color)
            logger.info(f"コントラスト比: {contrast_ratio:.2f}")
        else:
            logger.info(f"指定されたテキスト色を使用: {text_color}")
        
        # カラーパレットの可視化（余白の色とフォントの色を含む）
        palette_output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(output_path))[0]}_palette.png")
        self.color_analyzer.visualize_color_palette(palette, palette_output_path, 
                                                    margin_color=margin_dominant_color[:3],  # RGBのみを渡す
                                                    font_color=text_color)
        
        # 色空間の可視化
        color_space_output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(output_path))[0]}_color_space.png")
        self.color_analyzer.visualize_color_space(img, color_space_output_path, 
                                                  margin_color=margin_dominant_color[:3],  # RGBのみを渡す
                                                  font_color=text_color)
        
        logger.info("画像にテキストを描画中...")
        draw.text(position, tag, font=font, fill=text_color)
        
        logger.info(f"画像を保存中: {output_path}")
        img.save(output_path)
        logger.success(f"ヘッダー画像が正常に生成されました: {output_path}")
        
# 使用例
if __name__ == "__main__":
    image_service = ImageService()
    tag = "v1.0.0"
    output_dir = "output_images"
    font_name = ".github/release_notes/fonts/HigherJump-8MZ7M.ttf"
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 従来の手法でヘッダー画像を生成（自動色選択）
        # image_service.generate_header_image(tag, os.path.join(output_dir, "traditional_header_auto_color.png"), font_name, use_smooth_area=False, target_ratio=0.5)
        
        # 新しい余白検出手法でヘッダー画像を生成（自動色選択）
        image_service.generate_header_image(tag, os.path.join(output_dir, "smooth_area_header_auto_color.png"), font_name, use_smooth_area=True, target_ratio=0.8)
        
        # 色を指定してヘッダー画像を生成
        # image_service.generate_header_image(tag, os.path.join(output_dir, "custom_color_header.png"), font_name, use_smooth_area=True, target_ratio=0.8, text_color=(255, 0, 0))
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        logger.exception("詳細なエラー情報:")
