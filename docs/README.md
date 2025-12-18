# auth_gateway/__init__.py

from flask import Flask
from auth_gateway.config import Config
from auth_gateway.extensions import db, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.extensions['db'] = db
    app.extensions['migrate'] = migrate

    from auth_gateway.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app