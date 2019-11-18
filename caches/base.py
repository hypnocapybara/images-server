

class BaseCache:
    @staticmethod
    def get_image(image_hash: str, operations: str):
        raise NotImplemented

    @staticmethod
    def store_image(image, operations: str):
        raise NotImplemented
