import os

from main import app


def get_image(id):
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        if f'thumb-{id}-' in filename:
            return filename
    return 'default_thumb.jpg'


def remove_image(id):
    file = get_image(id)
    if file != 'default_thumb.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file))
