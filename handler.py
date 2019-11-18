from typing import Optional

from wand.image import Image


GRAVITY_MATCH = {
    'nw': 'north_west',
    'n': 'north',
    'ne': 'north_east',
    'w': 'west',
    'c': 'center',
    'e': 'east',
    'sw': 'south_west',
    's': 'south',
    'se': 'south_east',
}


def handle_crop(image: Image, params: str):
    gravity = params[:2]
    if gravity not in GRAVITY_MATCH:
        gravity = params[:1]
        if gravity not in GRAVITY_MATCH:
            gravity = 'c'
        else:
            params = params[1:]
    else:
        params = params[2:]

    width, height = [int(p) for p in params.split('x')]
    image.crop(width=width, height=height, gravity=GRAVITY_MATCH[gravity])


def process_image(source_image: Image, operations_string: str) -> Optional[Image]:
    operations = operations_string.split('/')
    image = source_image.clone()

    while len(operations) > 1:
        operation = operations.pop(0)
        params = operations.pop(0)

        if operation == 'crop':
            handle_crop(image, params)

        if operation == 'resize':
            image.transform(resize=params)

        if operation == 'rotate':
            image.rotate(int(params))

    return image
