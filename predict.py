from keras.models import load_model
from keras_preprocessing import image
import numpy as np
import os
os.environ['CUDA_VISIBLE_DEVICES'] = "0"


def make_prediction():
    loaded = load_model(os.path.join('model.h5'))
    test_image = image.load_img('test_images/1.jpg', target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = loaded.predict(test_image)
    if result[0][0] == 1:
        prediction = 'dog'
    else:
        prediction = 'cat'

    return prediction

