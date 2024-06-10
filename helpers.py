import os

from main import app


def get_image(id):
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        if filename == 'default_thumb.jpg':
            continue
        file_id = filename.rsplit('-')[1].rsplit('.')[0]
        if int(id) == int(file_id):
            return filename
    return 'default_thumb.jpg'
