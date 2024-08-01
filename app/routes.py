from flask import current_app as app
from flask import jsonify


@app.route('/')
def index():
    data = {
        'start': 'start page'
    }

    return jsonify(data)
