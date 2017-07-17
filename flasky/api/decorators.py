from flask_login import current_user
from flask import abort
from functools import wraps


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, *kwargs)

        return decorated_function

    return decorator
