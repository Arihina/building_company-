from flask import Blueprint, render_template

info_bp = Blueprint('info_bp', __name__)


@info_bp.route('/about')
@info_bp.route('/')
def index():
    return render_template('about.html'), 200
