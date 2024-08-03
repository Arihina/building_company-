from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import settings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.db_url
app.config['SECRET_KEY'] = settings.app_secret_key

db = SQLAlchemy(app)

with app.app_context():
    from . import routes
    from . import models
