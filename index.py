from flask import Flask
from predict import make_prediction
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/predict')
def predict():
    return make_prediction()



if __name__ == '__main__':
    app.run(port='5002')
