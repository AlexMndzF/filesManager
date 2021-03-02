import os
import ujson
from flask import request, Response, g, redirect, render_template, session, send_from_directory, flash, send_file

from filesManager.src.conectors import files
import filesManager.src.utils
from filesManager import settings as st
from filesManager.settings import app
from filesManager.src.conectors.users import check_login
from filesManager.src import authorization as auth, utils as u


@app.route('/', methods=['GET'])
def home():
    return render_template('_login.html')


@app.route('/login/', methods=['POST'])
def check_user():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        token = check_login(username=username, password=password)
    except TypeError:
        error = {'error': 'User not exist', 'code': 400}
        return render_template('error.html', error=error)
    if not token:
        error = {'error': 'Invalid user or password', 'code': 401}
        return render_template('error.html', error=error)
    session['token'] = token
    return redirect('/files/')


@app.route('/logout/')
def logout():
    session.pop('token')
    return render_template('_login.html')


@app.route('/files/upload/', methods=['POST'])
def upload_file():
    upload = request.files.get('upload')
    if not upload or upload.filename == '':
        return Response('Error no File')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ['.pdf', 'pdf']:
        return Response(response="Invalid file")
    try:
        files.upload_file(upload)
    except Exception as e:
        return Response(response=e.args)

    return redirect('/files/')


@app.route('/files/', methods=['GET'])
def get_files():
    result = filesManager.src.conectors.files.get_files()
    result = {'files': result}
    return render_template('table.html', items=result['files'])


@app.route('/files/<_id>/', methods=['DELETE'])
@auth.check_permissions(['delete data'])
def delete_file(_id):
    try:
        filesManager.src.conectors.files.delete_file(_id)
    except FileNotFoundError:
        error = {'error': 'File not found'}
        return Response(response=ujson.dumps(error), status=404)
    return redirect('/files/')


@app.route('/files/<_id>/', methods=['GET'])
def download_file(_id):
    try:
        file = files.get_by_id(_id)
    except FileNotFoundError:
        flash('File not found!')
    return send_file(file.path, as_attachment=True)


@app.before_request
def before_request():
    if request.path in ['/login/', "/"]:
        pass
    else:
        user_token = session.get('token')
        if not user_token:
            return render_template('error.html', error={'error': 'No Token', 'code': 401})
        else:
            user = u.decode_token(user_token)
            g.role = user['profile']
            g.token = user_token
            g.permissions = user['permissions']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in st.ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
