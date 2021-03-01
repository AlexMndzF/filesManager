from functools import wraps
from flask import g, Response


def check_permissions(permissions):
    """
    Decorador para compronar permisos
    """
    def check_permissions_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            user_token = g.token
            if not user_token:
                return Response(response='Sin token de autorizacion', status=403)
            elif g.role == 'admin':
                return func(*args, **kwargs)
            else:
                allowed = False
                user_perm = g.permissions
                perm = {e: True if e in user_perm else False for e in permissions}
                for permission in permissions:
                    allowed = allowed or perm[permission]
                if not allowed:
                    return Response(response='No autorizado', status=403)
            return func(*args, **kwargs)
        return func_wrapper
    return check_permissions_decorator
