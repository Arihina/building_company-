from flask import Blueprint

from .. import logger

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/admin', methods=['GET'])
def admin_page():
    logger.debug('/admin')
    return 'admin page'
