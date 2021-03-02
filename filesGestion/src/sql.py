from filesGestion.models import File
from filesGestion.settings import db


def get_id_from_username(username):
    _id = db.session.execute(f"Select u.id from users u where u.name = '{username}'").first()[0]
    return _id


def insert_document(file):
    file = File(name=file['name'], weigth=file['weigth'], hash=file['hash'], upload_date=file['upload_date'],
                path=file['path'])

    db.session.add(file)
    db.session.commit()
    return 200


