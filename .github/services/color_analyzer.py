# color_analyzer.py

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
from sklearn.cluster import KMeans
from loguru import logger
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist, squareform

from typing import Tuple, Optional, List

class ColorAnalyzer:
    def __init__(self, pixel_skip=2, color_similarity_threshold=0.999):
        self.pixel_skip = pixel_skip
        self.color_similarity_threshold = color_similarity_threshold

    def extract_color_palette_quadrants(self, image: Image.Image, n_colors: int = 40) -> list:
        """
        Extract a color palette by dividing the image into 4 quadrants,
        extracting colors from each, and then combining the results.
        Uses pixel sampling to reduce data size and removes similar colors.
        """
        logger.info(f"{self.pixel_skip}画素飛ばしサンプリングによるカラーパレット抽出を開始...")

        if image.mode == 'RGBA':
            image = image.convert('RGB')

        sampled_image = self.pixel_sampling(image)
        
        width, height = sampled_image.size
        mid_w, mid_h = width // 2, height // 2
        logger.info(f"{self.pixel_skip}画素飛ばしサンプリング結果 : {width}, {height}")
        
        quadrants = [
            (0, 0, mid_w, mid_h),
            (mid_w, 0, width, mid_h),
            (0, mid_h, mid_w, height),
            (mid_w, mid_h, width, height)
        ]

        all_colors = []

        for i, quad in enumerate(quadrants):
            logger.info(f"第{i+1}象限の処理中...")
            quadrant_img = sampled_image.crop(quad)
            logger.info(f"第{i+1}象限の画像 : {np.array(quadrant_img).shape}")
            quad_colors = self.extract_colors_from_quadrant(quadrant_img, n_colors // 4)
            all_colors.extend(quad_colors)

        logger.info("全象限の色を統合中...")
        kmeans = KMeans(n_clusters=n_colors, init='k-means++', n_init=10, max_iter=300, random_state=42)
        kmeans.fit(all_colors)
        initial_palette = kmeans.cluster_centers_.astype(int).tolist()

        logger.info("似た色を削除中...")
        final_palette = self.remove_similar_colors(initial_palette)

        logger.info(f"最終的なカラーパレット: {len(final_palette)} 色")
        return final_palette

    def pixel_sampling(self, image: Image.Image) -> Image.Image:
        """
        Sample pixels from the image to reduce its size.
        Handles both even and odd sized images.
        """
        width, height = image.size
        sampled_width = (width + self.pixel_skip - 1) // self.pixel_skip
        sampled_height = (height + self.pixel_skip - 1) // self.pixel_skip
        
        sampled_image = Image.new(image.mode, (sampled_width, sampled_height))
        pixels = image.load()
        sampled_pixels = sampled_image.load()

        for i in range(0, width, self.pixel_skip):
            for j in range(0, height, self.pixel_skip):
                sampled_pixels[i // self.pixel_skip, j // self.pixel_skip] = pixels[i, j]

        return sampled_image


    def extract_colors_from_quadrant(self, image: Image.Image, n_colors: int) -> list:
        """
        Extract colors from a single quadrant of the image.
        """
        pixels = np.array(image).reshape(-1, 3)
        logger.info(f"pixels: {len(pixels)}")
        # ピクセル数が多すぎる場合はさらにサンプリング
        if len(pixels) > 10000:
            indices = np.random.choice(len(pixels), 10000, replace=False)
            pixels = pixels[indices]

        kmeans = KMeans(n_clusters=n_colors, init='k-means++', n_init=5, max_iter=100, random_state=42)
        kmeans.fit(pixels)
        return kmeans.cluster_centers_
    

    def visualize_color_palette(self, palette: List[List[int]], output_path: str, 
                                margin_color: Optional[Tuple[int, int, int]] = None, 
                                font_color: Optional[Tuple[int, int, int]] = None):
        """
        Visualize the color palette and save it as an image.
        Colors are arranged in rows of 5, with additional rows for margin and font colors.
        """
        n_colors = len(palette)
        colors_per_row = 5
        n_rows = (n_colors + colors_per_row - 1) // colors_per_row  # Ceiling division
        n_cols = colors_per_row

        # 追加の行を確保（余白の色とフォントの色用）
        additional_rows = sum([margin_color is not None, font_color is not None])
        n_rows += additional_rows

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 2, n_rows * 2))
        fig.suptitle("Extracted Color Palette")

        # Ensure axes is always 2D for consistent indexing
        if n_rows == 1:
            axes = axes.reshape(1, -1)

        for i, color in enumerate(palette):
            row = i // colors_per_row
            col = i % colors_per_row
            ax = axes[row, col]

            rgb = tuple(color)
            hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb)
            ax.add_patch(plt.Rectangle((0, 0), 1, 1, facecolor=np.array(color)/255))
            ax.axis('off')
            ax.set_title(f'RGB: {rgb}\nHEX: {hex_color}', fontsize=8)

        # Margin Colorを追加（パレットの色の後の行）
        if margin_color is not None:
            margin_row = (n_colors + colors_per_row - 1) // colors_per_row
            for col in range(n_cols):
                ax = axes[margin_row, col]
                rgb = margin_color
                hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb)
                ax.add_patch(plt.Rectangle((0, 0), 1, 1, facecolor=np.array(rgb)/255))
                ax.axis('off')
                if col == 0:
                    ax.set_title(f'Margin Color\nRGB: {rgb}\nHEX: {hex_color}', fontsize=8)

        # Font Colorを追加（Margin Colorの後の行、またはパレットの色の後の行）
        if font_color is not None:
            font_row = n_rows - 1
            for col in range(n_cols):
                ax = axes[font_row, col]
                rgb = font_color
                hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb)
                ax.add_patch(plt.Rectangle((0, 0), 1, 1, facecolor=np.array(rgb)/255))
                ax.axis('off')
                if col == 0:
                    ax.set_title(f'Font Color\nRGB: {rgb}\nHEX: {hex_color}', fontsize=8)

        # Remove any unused subplots
        for i in range(n_colors, (n_rows - additional_rows) * n_cols):
            row = i // colors_per_row
            col = i % colors_per_row
            fig.delaxes(axes[row, col])

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"カラーパレットを保存しました: {output_path}")
        

    def visualize_color_space(self, image: Image.Image, output_path: str, sample_size: int = 500000, n_clusters: int = 1000,
                              margin_color: Optional[Tuple[int, int, int]] = None, 
                              font_color: Optional[Tuple[int, int, int]] = None):
        """
        Visualize the color space of the image in 3D XYZ coordinates, skipping similar colors.
        """
        logger.info("色空間の可視化を開始...")

        # Resize and sample pixels
        img_array = np.array(image.convert('RGB').resize((100, 100)))
        pixels = img_array.reshape(-1, 3)
        logger.debug(f"元のピクセル数: {len(pixels)}")

        if len(pixels) > sample_size:
            indices = np.random.choice(len(pixels), sample_size, replace=False)
            pixels = pixels[indices]

        logger.debug(f"サンプリング後のピクセル数: {len(pixels)}")

        # Use K-means clustering to group similar colors
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get the cluster centers (representative colors)
        representative_colors = kmeans.cluster_centers_.astype(int)
        
        logger.debug(f"代表的な色の数: {len(representative_colors)}")

        # Convert RGB to XYZ
        xyz = np.array([self.rgb_to_xyz(rgb) for rgb in representative_colors])

        # Create 3D plot
        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(111, projection='3d')

        # Plot points
        scatter = ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], c=representative_colors/255, s=8)

        # Add margin color and font color if provided
        if margin_color is not None:
            margin_xyz = self.rgb_to_xyz(margin_color)
            ax.scatter(margin_xyz[0], margin_xyz[1], margin_xyz[2], c="blue", s=200, marker='s', label='Margin Color')

        if font_color is not None:
            font_xyz = self.rgb_to_xyz(font_color)
            ax.scatter(font_xyz[0], font_xyz[1], font_xyz[2], c="red", s=200, marker='^', label='Font Color')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Color Space Visualization (XYZ) - Top-down View')

        # Set the view to top-down
        ax.view_init(elev=50, azim=-80)

        # Adjust axis limits for better visualization
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.set_zlim(0, 100)

        # Add colorbar
        cbar = plt.colorbar(scatter)
        cbar.set_label('RGB Color')

        # Add legend
        if margin_color is not None or font_color is not None:
            ax.legend()

        # Save the plot
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"色空間の可視化を保存しました: {output_path}")
        
    def get_contrasting_color(self, background_color: tuple) -> tuple:
        """
        Determine if a color is light or dark and return a contrasting color.
        """
        luminance = (0.299 * background_color[0] + 0.587 * background_color[1] + 0.114 * background_color[2]) / 255
        return (0, 0, 0) if luminance > 0.5 else (255, 255, 255)
    

    def rgb_to_xyz(self, rgb):
        """
        Convert RGB values to XYZ color space.
        """
        rgb = np.array(rgb[:3]) / 255.0  # RGBの3つの値のみを使用し、0-1の範囲に正規化
        mask = rgb > 0.04045
        rgb[mask] = ((rgb[mask] + 0.055) / 1.055) ** 2.4
        rgb[~mask] /= 12.92

        rgb = rgb * 100
        xyz = np.dot(rgb, np.array([
            [0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1191920, 0.9503041]
        ]))
        return xyz

    def get_contrasting_color(self, background_color: tuple) -> tuple:
        """
        Determine if a color is light or dark and return a contrasting color.
        """
        luminance = (0.299 * background_color[0] + 0.587 * background_color[1] + 0.114 * background_color[2]) / 255
        return (0, 0, 0) if luminance > 0.5 else (255, 255, 255)


    def remove_similar_colors(self, colors: list) -> list:
        """
        Remove similar colors from the palette based on RGB vector similarity.
        """
        unique_colors = []
        for color in colors:
            if not any(self.color_similarity(color, uc) > self.color_similarity_threshold for uc in unique_colors):
                unique_colors.append(color)
        return unique_colors

    def color_similarity(self, color1: list, color2: list) -> float:
        """
        Calculate cosine similarity between two color vectors in RGB space.
        """
        dot_product = np.dot(color1, color2)
        norm_product = np.linalg.norm(color1) * np.linalg.norm(color2)
        return dot_product / norm_product if norm_product != 0 else 0

if __name__ == "__main__":
    # pixel_skipを3に設定してColorAnalyzerのインスタンス化
    analyzer = ColorAnalyzer(pixel_skip=4)

    # サンプル画像のパス（実際の画像パスに置き換えてください）
    sample_image_path = r".github\release_notes\assets\release_notes_header_image_06.png"

    # 出力ディレクトリの作成
    output_dir = "color_analysis_output"
    os.makedirs(output_dir, exist_ok=True)

    try:
        # 画像を開く
        with Image.open(sample_image_path) as img:
            # 4分割法でカラーパレットの抽出と可視化
            palette = analyzer.extract_color_palette_quadrants(img, n_colors=40)
            palette_output_path = os.path.join(output_dir, "color_palette_quadrants_sampled.png")
            analyzer.visualize_color_palette(palette, palette_output_path)

            # 色空間の可視化
            color_space_output_path = os.path.join(output_dir, "color_space_sampled.png")
            analyzer.visualize_color_space(img, color_space_output_path)

        logger.success("色分析が完了しました。結果は {} ディレクトリに保存されています。".format(output_dir))

        # 最も支配的な色（パレットの最初の色）に基づいてコントラストの高い色を取得
        dominant_color = tuple(palette[0])
        contrasting_color = analyzer.get_contrasting_color(dominant_color)
        logger.info(f"最も支配的な色: RGB{dominant_color}, コントラストの高い色: RGB{contrasting_color}")

    except FileNotFoundError:
        logger.error(f"指定された画像ファイルが見つかりません: {sample_image_path}")
    except Exception as e:
        logger.exception(f"色分析中にエラーが発生しました: {str(e)}")
