import datetime
import os

from werkzeug.utils import secure_filename

from filesManager.models import File
from filesManager.settings import UPLOAD_FOLDER
from filesManager.settings import db
from filesManager.src import utils as u
from filesManager.src import sql


def upload_file(upload_file):
    filename = secure_filename(upload_file.filename)
    file = os.path.join(UPLOAD_FOLDER, filename)
    upload_file.save(file)
    has_file = u.has_file(file)
    size = os.stat(file).st_size
    file_to_upload = {
        'name': str(filename),
        'weigth': float(size),
        'hash': str(has_file),
        'path': str(file),
        'upload_date': datetime.datetime.now()
    }
    sql.insert_document(file_to_upload)

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


def get_by_id(_id):
    file = File.query.get(_id)
    if not file:
        raise FileNotFoundError
    return file