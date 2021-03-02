from filesGestion.models import User
from filesGestion.src.sql import get_id_from_username
from filesGestion.src.utils import generate_token


def check_login(username, password):
    user = check_user(username)

    if user.password == password:
        user = {
            'userId': user.id,
            'name': user.name,
            'profile': user.profile,
            'permissions': [e for e in user.permissions.split(',')]
        }
        token = generate_token(user)
        return token
    else:
        return 'Invalid password'


def check_user(username):
    _id = get_id_from_username(username)
    user = User.query.get(_id)
    return user