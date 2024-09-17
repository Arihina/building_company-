import json
import logging.config
import os
from logging import getLogger

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import settings

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = settings.db_url
app.config['SECRET_KEY'] = settings.app_secret_key

db = SQLAlchemy(app)
login_manager = LoginManager(app)
CORS(app)

current_dir = os.path.dirname(os.path.abspath(__file__))
logger_config = os.path.join(current_dir, 'logger.config')

with open(logger_config) as file:
    cfg = json.load(file)

logging.config.dictConfig(cfg)
logger = getLogger()

with app.app_context():
    from .routes.employees import employees_bp
    from .routes.clients import clients_bp
    from .routes.products import products_bp
    from .routes.drivers import drivers_bp
    from .routes.warehouses import warehouses_bp
    from .routes.consists import consists_bp
    from .routes.contracts import contracts_bp
    from .routes.orders import orders_bp
    from .routes.managers import managers_bp
    from .routes.info import info_bp
    from .routes.admin import admin_bp
    from .routes.errors import errors_bp
    from .routes.authentication import auth_bp

    app.register_blueprint(employees_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(drivers_bp)
    app.register_blueprint(warehouses_bp)
    app.register_blueprint(consists_bp)
    app.register_blueprint(contracts_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(managers_bp)
    app.register_blueprint(info_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp)

    from . import models
