from filesManager.models import File
from filesManager.settings import db
from filesManager.src.exceptions import UserNotExistException


def get_id_from_username(username):
    try:
        _id = db.session.execute(f"Select u.id from users u where u.name = '{username}'").first()[0]
    except TypeError:
        raise UserNotExistException()
    return _id


def insert_document(file):
    file = File(name=file['name'], weigth=file['weigth'], hash=file['hash'], upload_date=file['upload_date'],
                path=file['path'])

    db.session.add(file)
    db.session.commit()
    return 200


