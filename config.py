from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from logging.config import dictConfig
from flask_cors import CORS

app = Flask(__name__)
app.config['ENV'] = 'PRODUCTION'
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})