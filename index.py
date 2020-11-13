from flask import Flask, request
from flask_http_response import success, result, error
from werkzeug.utils import secure_filename
from utils import find_file, _download, allowed_file, make_prediction, logger, check_for_link
from os import path
from config import app

@app.route('/')
def hello_world():
    logger('Server root', request)
    return 'hello all possible worlds --- -- - ***'


@app.route('/predict/', methods=['POST'])
def predict():
    is_link = check_for_link(request)
    name = request.form['name'].replace(' ', '_')
    if is_link:
        file = _download(name)
        if file['success']:
            prediction = str(make_prediction(file['name']))
            logger('Successful prediction', request)
            return success.return_response(message=prediction, status=200)
        else:
            logger('Faulty link', request)
            return error.return_response(message='Link is not correct', status=400)
    if find_file(name):
        prediction = str(make_prediction(name))
        logger('Successful prediction', request)
        return success.return_response(message=prediction, status=200)
    else:
        logger('File not found', request)
        return error.return_response(message='File not found', status=404)


@app.route('/upload/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['image']
        if allowed_file(f.filename):
            f.save(path.join('assets/uploads/') + secure_filename(f.filename))
            logger('Image uploaded', request)
            return success.return_response(message='Upload completed', status=200)
        else:
            logger('Inpropriate file', request)
            return error.return_response(message='Inpropriate file', status=400)


if __name__ == '__main__':
    from waitress import serve
    print('Love is forever...')
    serve(app, host="0.0.0.0", port=4000)

    