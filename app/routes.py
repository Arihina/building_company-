from flask import current_app as app
from flask import jsonify
from sqlalchemy import text

from . import db


@app.route('/')
def index():
    version_query = db.session.execute(text("SELECT version()")).fetchone()
    postgres_version = version_query[0] if version_query else "Unknown"

    data = {
        'postgresql version': postgres_version
    }

    return jsonify(data)
