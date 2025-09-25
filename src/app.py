from flask import Flask

from src.error_handlers import error_handlers_blueprint
from src.router import api_blueprint


def create_app(name: str):
    app = Flask(name)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(error_handlers_blueprint)
    return app
