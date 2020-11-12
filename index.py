from flask import Flask, request
from predict import make_prediction
from flask_http_response import success, result, error
from werkzeug.utils import secure_filename
from os import path
from search import find_file
from download_image import _download

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/predict/<is_link>/<name>/', methods=['GET', 'POST']) 
def predict(is_link, name):
    if is_link == 'True':
        print('is link tho')
        file = _download(name)
        if file['success']:
            prediction = str(make_prediction(file['name']))
            return success.return_response(message=prediction, status=200)
        else:
            return error.return_response(message='Link is not correct', status=400)
    if find_file(name):
        prediction = str(make_prediction(name))
        return success.return_response(message=prediction, status=200)
    else:
        return error.return_response(message='File not found', status=404)


@app.route('/upload/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['image']
        f.save(path.join('assets/uploads/') + secure_filename(f.filename))
    return success.return_response(message='Upload completed', status=200)


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=4000)
    