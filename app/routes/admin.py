from flask import Blueprint, render_template
from flask_login import login_required

from .. import logger

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/admin', methods=['GET'])
@login_required
def admin_page():
    logger.debug('/admin')
    return render_template('admin_page.html'), 200
