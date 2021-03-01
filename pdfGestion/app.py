import datetime
import os

from flask import request, Response, g
from werkzeug.utils import secure_filename

from pdfGestion import settings as st
from pdfGestion.settings import app
from pdfGestion.src import sql, authorization as auth, utils as u


@app.route('/login/', methods=['POST'])
def check_user():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        token = sql.check_loging(username=username, password=password)
    except TypeError as e:
        return Response(response="User not exist", status=400)
    return Response(response=token, status=200)


@app.route('/pdf/upload/', methods=['POST'])
def upload_file():
    upload = request.files.get('upload')
    if not upload or upload.filename == '':
        return Response('Error no File')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ['.pdf', 'pdf']:
        return Response(response="Invalid file")
    filename = secure_filename(upload.filename)
    try:
        file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        upload.save(file)
        has_file = u.has_file(file)
    except Exception as e:
        return Response(response=(e.content), status=e.status)
    size = os.stat(file).st_size
    file_to_upload = {
        'name': str(filename),
        'weigth': float(size),
        'hash': str(has_file),
        'path': str(file),
        'upload_date': datetime.datetime.now()
    }
    try:
        sql.insert_document(file_to_upload)
    except Exception as e:
        e
    return Response(response='', status=200)


@app.route('/pdf/upload/', methods=['GET'])
def upload_pdfs_get():
    return """
        <form class="form_but"  action="/pdf/upload/" method="post" enctype="multipart/form-data">
                <label class="but_red" for="file"> <p class="lc">Select file</p></label>
                <input id="file" class="inputfile" type="file" name="upload" />
                <label class="but_red" for="upload"> <p class="lc">Upload</p></label>
                <input class="inputfile" id="upload" type="submit"/>
              </form>
        """


@app.route('/pdf/', methods=['GET'])
def get_pdfs():
    pass


@app.route('/pdf/<id>/', methods=['DELETE'])
@auth.check_permissions(['delete data'])
def delete_pdfs(id):
    pass

# @app.before_request
def before_request():
    if request.path in ['/login/']:
        pass
    else:
        user_token = request.headers.get('Authorization')
        if not user_token:
            raise FileNotFoundError(message='No token', status_code=401)
        else:
            user = sql.decode_token(user_token)
            g.role = user['profile']
            g.token = user_token
            g.permissions = user['permissions']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in st.ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
