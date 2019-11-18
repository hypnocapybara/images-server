import os
import hashlib
from typing import Optional

from wand.image import Image

from .base import BaseCache


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FileSystemCache(BaseCache):
    @staticmethod
    def get_image(image_hash: str, operations: str) -> Optional[Image]:
        directory = image_hash[:2]
        operations_hash = hashlib.md5(operations.encode('utf-8')).hexdigest()
        filename = image_hash[2:] + '-' + operations_hash
        image_path = os.path.join(BASE_DIR, 'uploads', 'cache', directory, filename)
        if not os.path.exists(image_path):
            return None

        return Image(filename=image_path)

    @staticmethod
    def store_image(image: Image, image_hash: str, operations: str):
        directory = image_hash[:2]
        upload_dir = os.path.join(BASE_DIR, 'uploads', 'cache', directory)
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        operations_hash = hashlib.md5(operations.encode('utf-8')).hexdigest()
        filename = image_hash[2:] + '-' + operations_hash

        full_path = os.path.join(upload_dir, filename)
        image.save(filename=full_path)
