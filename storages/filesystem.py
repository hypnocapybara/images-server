import os
import random
import hashlib
from typing import Optional

from wand.image import Image

from .base import BaseStorage


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FileSystemStorage(BaseStorage):
    @staticmethod
    def get_image(image_hash: str) -> Optional[Image]:
        directory = image_hash[:2]
        filename = image_hash[2:]
        image_path = os.path.join(BASE_DIR, 'uploads', directory, filename)
        if not os.path.exists(image_path):
            return None

        return Image(filename=image_path)

    @staticmethod
    def store_image(image: Image):
        uploads_dir = os.path.join(BASE_DIR, 'uploads')
        if not os.path.exists(uploads_dir):
            os.mkdir(uploads_dir)

        image_hash_base = '{0}-{1}'.format(image.signature, random.random())
        image_hash = hashlib.sha1(image_hash_base.encode('utf-8')).hexdigest()
        directory = image_hash[:2]
        filename = image_hash[2:]

        upload_dir = os.path.join(uploads_dir, directory)
        if not os.path.exists(upload_dir):
            os.mkdir(upload_dir)

        full_path = os.path.join(upload_dir, filename)
        image.save(filename=full_path)
        return image_hash

    @staticmethod
    def delete_image(image_hash: str):
        directory = image_hash[:2]
        filename = image_hash[2:]
        upload_file = os.path.join(BASE_DIR, 'uploads', directory, filename)
        result = os.path.exists(upload_file)
        if result:
            os.remove(upload_file)

        return result
