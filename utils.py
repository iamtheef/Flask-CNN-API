import os
from flask import request
from flask_http_response import success, error
from pathlib import Path
import requests
import uuid
from config import app

_images = os.path.join('assets/uploads/')


def find_file(filename):
    for root, dirs, files in os.walk(_images):
            if filename in files:
                return True
    return False


def remove_file(filename):
    try:
        os.remove(os.path.join(_images + filename))
        return True
    except:
        return False
            

def _download(url):
    _filename = str(uuid.uuid4())
    try:
        Path(os.path.join(_images + _filename + '.jpg')).touch()
        f = open(os.path.join(_images + _filename + '.jpg'), 'wb')
        f.write(requests.get(url).content)
        f.close()
        return {'success': True, 'name': _filename + '.jpg'}
    except:
        remove_file(_filename + '.jpg')
        return {'success': False, 'name': None}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}
           
           
def logger(msg, req):
    return app.logger.info(str(msg + ' ' + str(req)))

           
from keras.models import load_model
from keras_preprocessing import image
import numpy as np
import os
os.environ['CUDA_VISIBLE_DEVICES'] = "0"


def make_prediction(name):
    loaded = load_model(os.path.join('assets/model_30.h5'), compile=False)
    test_image = image.load_img(os.path.join(_images + name), target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = loaded.predict(test_image)

    if app.config['ENV'] != 'TESTING':
        remove_file(name)
    return 'cat' if result[0][0] == 0 else 'dog'


def call_prediction(input):
    try:
        prediction = make_prediction(input)
        logger('Successful prediction', request)
        return success.return_response(message=prediction, status=200)
    except:
        logger('Problem appeared ', request)
        remove_file(input)
        return error.return_response(message='Something went wrong', status=204)