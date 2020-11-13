import os
from pathlib import Path
import requests
import uuid
from config import app


search_path = os.path.join('assets/uploads/')

def find_file(filename):
    for root, dirs, files in os.walk(search_path):
            if filename in files:
                return True
    return False
            

def _download(url):
    _filename = str(uuid.uuid4())
    try:
        Path(os.path.join('assets/uploads/'+ _filename + '.jpg')).touch()
        myfile = requests.get(url)
        open(os.path.join('assets/uploads/'+ _filename + '.jpg'), 'wb').write(myfile.content)
        return {'success': True, 'name': _filename + '.jpg'}
    except:
        os.remove(os.path.join('assets/uploads/'+ _filename + '.jpg'))
        return {'success': False, 'name': None}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}
           
           
def logger(msg, req):
    return app.logger.info(str(msg + ' ' + str(req)))

def check_for_link(req):
    if req.form['is_link'] in ['true', 'True']:
        return True
    else: return False

           
from keras.models import load_model
from keras_preprocessing import image
import numpy as np
import os
os.environ['CUDA_VISIBLE_DEVICES'] = "0"


def make_prediction(name):
    loaded = load_model(os.path.join('assets/model.h5'))
    test_image = image.load_img(os.path.join('assets/uploads/'+ name), target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = loaded.predict(test_image)
    
    os.remove(os.path.join('assets/uploads/'+ name))
    return result[0][0]
