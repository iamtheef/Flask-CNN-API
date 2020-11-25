from flask import request
from flask_cors import cross_origin
from flask_http_response import success, error
from werkzeug.utils import secure_filename
from utils import find_file, _download, allowed_file, logger, call_prediction
from os import path
from config import app


@app.route('/')
def hello_world():
    logger('Server root', request)
    return success.return_response(message='hello all possible worlds --- -- - ***', status=200)


@app.route('/predict/', methods=['POST'])
@cross_origin()
def predict():
    return str(request)
    # try:
    #     is_link = request.get_json()['isLink']
    #     name = request.get_json()['input'].replace(' ', '_')
    #     if is_link:
    #         file = _download(name)
    #         if file['success']:
    #             return call_prediction(file['name'])
    #         else:
    #             logger('Faulty link', request)
    #             return error.return_response(message='Link is not correct', status=400)
    #     elif find_file(name):
    #         return call_prediction(name)
    #     else:
    #         logger('File not found', request)
    #         return error.return_response(message='File not found', status=404)
    # except:
    #     return error.return_response(message='Something was wrong', status=500)


@app.route('/upload/', methods=['POST'])
@cross_origin()
def upload_file():
    try:
        f = request.files['image']
        if allowed_file(f.filename):
            f.save(path.join('assets/uploads/') + secure_filename(f.filename))
            logger('Image uploaded', request)
            return success.return_response(message='Upload completed', status=200)
        else:
            logger('Inpropriate file', request)
            return error.return_response(message='Inpropriate file', status=400)

    except:
        return error.return_response(message='Something was wrong', status=500)


if __name__ == '__main__':
    from waitress import serve

    app.config['CORS_HEADERS'] = 'Content-Type'
    print('Love is forever...')
    serve(app, listen='*:4000')

