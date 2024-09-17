from functools import wraps

from flask import abort
from flask_login import current_user


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.post != 'admin':
            return abort(403)
        return func(*args, **kwargs)

    return wrapper


def manager_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.post != 'manager':
            return abort(403)
        return func(*args, **kwargs)

    return wrapper
