import os

from filesGestion.models import File
from filesGestion.settings import db


def upload_file(file):
    pass

def remove_file(path):
    if os.path.isfile(path):
        os.remove(path)
    else:
        raise FileNotFoundError


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