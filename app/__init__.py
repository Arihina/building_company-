from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import settings

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.db_url
app.config['SECRET_KEY'] = settings.app_secret_key

db = SQLAlchemy(app)

with app.app_context():
    from .routes.employees import employees_bp
    from .routes.clients import clients_bp
    from .routes.products import products_bp
    from .routes.drivers import drivers_bp
    from .routes.info import info_bp

    app.register_blueprint(employees_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(drivers_bp)
    app.register_blueprint(info_bp)

    from . import models
