from filesGestion.models import User, File
from jose import jwt
from filesGestion.settings import db
from filesGestion.src.conectors.files import remove_file


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


def insert_document(file):
    file = File(name=file['name'], weigth=file['weigth'], hash=file['hash'], upload_date=file['upload_date'],
                path=file['path'])

    db.session.add(file)
    db.session.commit()
    return 200


def get_files():
    result = File.query.all()
    files = []
    for e in result:
        file = {
            'id': e.id,
            'name': e.name,
            'size': e.weigth,
            'hash': e.hash,
            'upload_date': e.upload_date.strftime("%m/%d/%Y, %H:%M"),
            'path': e.path
        }
        files.append(file)
    return files


def delete_file(_id):
    file = File.query.get(_id)
    if not file:
        raise FileNotFoundError
    remove_file(file.path)
    db.session.delete(file)
    db.session.commit()
