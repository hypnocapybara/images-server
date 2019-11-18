import io
from flask import Flask, request, send_file
from wand.image import Image

from storages import default_storage
from caches import default_cache
from handler import process_image


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/image/<path:image_hash_and_operations>')
def view_image(image_hash_and_operations):
    if '/' in image_hash_and_operations:
        image_hash, operations = image_hash_and_operations.split('/', 1)
    else:
        image_hash = image_hash_and_operations
        operations = None

    image = default_cache.get_image(image_hash, operations)
    if image:
        return send_file(io.BytesIO(image.make_blob()), mimetype=image.mimetype)

    image = default_storage.get_image(image_hash)
    if not image:
        return {
            'status': 'error',
            'message': 'image not found: {0}'.format(image_hash)
        }, 404

    if operations:
        image = process_image(image, operations)
        if not image:
            return {
                'status': 'error',
                'message': 'bad operations: {0}'.format(operations)
            }, 400
        default_cache.store_image(image, image_hash, operations)

    return send_file(io.BytesIO(image.make_blob()), mimetype=image.mimetype)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    with Image(file=f) as image:
        image_hash = default_storage.store_image(image)
        return {
            'status': 'success',
            'hash': image_hash
        }
