from pdfGestion.models import User, Pdf
from jose import jwt
from pdfGestion.app import db

def check_user(username):
    _id = get_id_from_username(username)
    user = User.query.get(_id)
    return user


def get_id_from_username(username):
    _id = db.session.execute(f"Select u.id from users u where u.name = '{username}'").first()[0]
    return _id


def generate_token(user):
    secret = 'amf1234'
    algorithm = 'HS256'
    token = jwt.encode(user, secret, algorithm)
    return token


def decode_token(token):
    secret = 'amf1234'
    algorithm = 'HS256'
    user = jwt.decode(token, secret, algorithm)
    return user


def check_loging(username, password):
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