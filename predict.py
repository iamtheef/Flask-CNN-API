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
    
    # os.remove(os.path.join('assets/uploads/'+ name))
    return result[0][0]

