from flask_pymongo import PyMongo


def init_app(app):
    global mongo

    mongo = PyMongo(app)
    mongo.init_app(app)
