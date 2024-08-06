from flask import Blueprint, jsonify
from sqlalchemy import text

from .. import db

info_bp = Blueprint('info_bp', __name__)


@info_bp.route('/')
def index():
    version_query = db.session.execute(text("SELECT version()")).fetchone()
    postgres_version = version_query[0] if version_query else "Unknown"

    data = {
        'postgresql version': postgres_version,
        'flask version': '3.0.3'
    }

    return jsonify(data)
