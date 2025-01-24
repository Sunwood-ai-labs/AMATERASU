"""
ルーティングパッケージ
"""
from .generate import create_generate_page
from .cache import create_cache_page
from .cloudfront import create_cloudfront_page

__all__ = [
    'create_generate_page',
    'create_cache_page',
    'create_cloudfront_page'
]
