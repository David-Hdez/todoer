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
        SECRET_KEY='mykey',
        DATABASE_HOST=os.environ.get('TODOER_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('TODOER_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('TODOER_DATABASE_USER'),
        DATABASE=os.environ.get('TODOER_DATABASE')
    )

    @app.route('/tests')
    def hello():
        return 'Hello, World!'

    return app
