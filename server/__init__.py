import logging
import setting
from flask import Flask
from wsgiref.simple_server import make_server
from .views.paper import paper
from utils.log_handler import flask_log_handler


app = Flask(__name__)
app.register_blueprint(paper, url_prefix='/paper')

def run_server():
    with make_server(setting.HOST, setting.PORT, app) as httpd:
        print('Serving on port {}...'.format(setting.PORT))
        httpd.serve_forever()