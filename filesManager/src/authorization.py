from functools import wraps
from flask import g, render_template


def check_permissions(permissions):
    """
    Decorador para compronar permisos
    """
    def check_permissions_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            user_token = g.token
            if not user_token:
                error = {'error': 'No token provided', 'code': 403}
                return render_template('error.html', error=error)
            elif g.role == 'admin':
                return func(*args, **kwargs)
            else:
                allowed = False
                user_perm = g.permissions
                perm = {e: True if e in user_perm else False for e in permissions}
                for permission in permissions:
                    allowed = allowed or perm[permission]
                if not allowed:
                    error = {'error': 'Not authorized', 'code': 403}
                    return render_template('error.html', error=error)
            return func(*args, **kwargs)
        return func_wrapper
    return check_permissions_decorator
