from flask import Flask, redirect, url_for, current_app
import logging


def create_app(config, debug=False, testing=False):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model.
    with app.app_context():
        model = get_model()
        model.init_app(app)

    # Register the jupez CRUD blueprint
    from .crud import crud
    app.register_blueprint(crud, url_prefix='/jupes')

    # Add a default root route.
    @app.route("/")
    def index():
        return redirect(url_for('crud.list'))

    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occured: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app


def get_model():
    model_backend = current_app.config['DATA_BACKEND']
    if model_backend == 'cloudsql':
        from . import model_cloudsql
        model = model_cloudsql
    elif model_backend == 'mongodb':
        from . import mongodb
        model = mongodb
    else:
        raise ValueError(
            "No appropriate databackend configured. "
            "Please specify datastore, cloudsql, or mongodb")

    return model
