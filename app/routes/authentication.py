from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import logout_user, current_user, login_user, login_required

from app import login_manager
from .. import models
from ..services.UserLogin import User

auth_bp = Blueprint('auth_bp', __name__)


@login_manager.user_loader
def load_user(user_id):
    empl = models.Employee.query.get(user_id)
    if empl:
        return User(empl.email, empl.post, empl.id)


@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('managers_bp.profile', id=current_user.get_id()))

    if request.method == 'POST':
        email = str(request.form.get('email'))
        employee = models.Employee.query.filter_by(email=str(email)).first()
        if employee:
            user = load_user(employee.id)
            login_user(user)
            if user.get_post() == 'manager':
                return redirect(request.args.get('next') or url_for('managers_bp.profile',
                                                                    id=current_user.get_id()))
            else:
                return redirect(request.args.get('next') or url_for('admin_bp.admin_page'))
    return render_template('login.html'), 200


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))
