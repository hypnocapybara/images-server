import io
import hashlib
from urllib.request import urlopen

from flask import Flask, request, send_file
from wand.image import Image
from wand.exceptions import WandException

from storages import default_storage
from caches import default_cache
from handler import process_image


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/image/<path:image_hash_and_operations>', methods=['GET'])
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
    if 'file' not in request.files:
        return {
            'status': 'error',
            'message': 'no file provided'
        }, 400

    f = request.files['file']

    try:
        with Image(file=f) as image:
            image_hash = default_storage.store_image(image)
            return {
                'status': 'success',
                'hash': image_hash
            }
    except WandException:
        return {
            'status': 'error',
            'message': 'image processing error'
        }, 400


@app.route('/image/<path:image_hash>', methods=['DELETE'])
def delete_image(image_hash):
    default_cache.delete_image(image_hash)
    deleted = default_storage.delete_image(image_hash)
    if deleted:
        return {
            'status': 'success'
        }
    else:
        return {
            'status': 'error',
            'message': 'file not found'
        }, 404


@app.route('/external', methods=['GET'])
def external():
    url = request.args.get('url')
    operations = request.args.get('operations')
    assert url and operations

    reset_cache = request.args.get('reset_cache') == '1'
    image_hash = hashlib.sha1(url.encode('utf-8')).hexdigest()

    if not reset_cache:
        image = default_cache.get_image(image_hash, operations)
        if image:
            return send_file(io.BytesIO(image.make_blob()), mimetype=image.mimetype)

    response = urlopen(url)
    f = io.BytesIO(response.read())

    with Image(file=f) as image:
        if operations:
            image = process_image(image, operations)
            if not image:
                return {
                    'status': 'error',
                    'message': 'bad operations: {0}'.format(operations)
                }, 400
            default_cache.store_image(image, image_hash, operations)

        return send_file(io.BytesIO(image.make_blob()), mimetype=image.mimetype)
