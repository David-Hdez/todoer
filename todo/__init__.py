import os
from flask import Flask


def create_app():
    """Application Factories


    Help to do testing.
    Create instances of the app.
    """
    app = Flask(__name__)
    # Variables de entorno para configurar
    # SECRET_KEY define las sesiones para la aplicacion
    app.config.from_mapping(
        SECRET_KEY='b328kQ3U8R55Xh',
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE')
    )

    from . import db
    # app created to init_app for configuration
    db.init_app(app)

    @app.route('/tests')
    def hello():
        return 'Hello, World!'

    return app
