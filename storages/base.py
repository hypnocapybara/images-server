from typing import Optional

from wand.image import Image


class BaseStorage:
    @staticmethod
    def get_image(image_hash: str) -> Optional[Image]:
        raise NotImplemented

    @staticmethod
    def store_image(image: Image) -> str:
        raise NotImplemented
