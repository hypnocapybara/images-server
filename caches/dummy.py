from typing import Optional
from wand.image import Image

from .base import BaseCache


class DummyCache(BaseCache):
    @staticmethod
    def get_image(image_hash: str, operations: str) -> Optional[Image]:
        return None

    @staticmethod
    def store_image(image, operations: str):
        return
