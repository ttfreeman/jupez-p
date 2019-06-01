from flask import Flask
from . import mongodb


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    model = mongodb
    model.init_app(app)
