from flask import current_app as app
from flask import jsonify
from sqlalchemy import text, select
from pprint import pprint

from . import db
from . import models


@app.route('/')
def index():
    version_query = db.session.execute(text("SELECT version()")).fetchone()
    postgres_version = version_query[0] if version_query else "Unknown"

    data = {
        'postgresql version': postgres_version
    }

    return jsonify(data)


@app.route('/employees', methods=['GET'])
def get_employees():
    query = (
        select(models.Employee)
    )
    employee = db.session.execute(query).scalars().all()
    pprint(employee)

    return 'OK', 200

