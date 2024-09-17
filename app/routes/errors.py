from flask import render_template, Blueprint

errors_bp = Blueprint('errors_bp', __name__)


@errors_bp.app_errorhandler(400)
def bad_request(error):
    return render_template('400.html'), 400


@errors_bp.app_errorhandler(401)
def unauthorized(error):
    return render_template('401.html'), 401


@errors_bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403


@errors_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@errors_bp.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
