from flask import request, g, redirect, render_template, session, flash, send_file, Response

from filesManager.src.conectors import files
import filesManager.src.utils
from filesManager.settings import app
from filesManager.src.conectors.users import check_login
from filesManager.src import authorization as auth, utils as u
from flask_paginate import Pagination, get_page_parameter

from filesManager.src.exceptions import FileAlreadyInPath


@app.route('/', methods=['GET'])
def home():
    if not session.get('token'):
        navbar=True
    navbar=False
    return render_template('login_page.html', navBar=navbar)


@app.route('/login/', methods=['POST'])
def check_user():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        token = check_login(username=username, password=password)
    except TypeError:
        error = {'error': 'User not exist', 'code': 400}
        return render_template('error.html', error=error, navBar=True)
    if not token:
        error = {'error': 'Invalid user or password', 'code': 401}
        return render_template('error.html', error=error, navBar=True)
    session['token'] = token
    return redirect('/files/')


@app.route('/logout/', methods=['POST'])
def logout():
    session.pop('token')
    return Response(status=200)


@app.route('/files/upload/', methods=['POST'])
def upload_file():
    upload = request.files.get('upload')
    if not upload or upload.filename == '':
        return redirect('/files/')
    try:
        files.upload_file(upload)
    except FileAlreadyInPath:
        error = {'error': 'File already exist', 'code': 409}
        return render_template('error.html', error=error, navBar=True)
    except Exception as e:
        error = {'error': e.args, 'code': ""}
        return render_template('error.html', error=error, navBar=True)


    return redirect('/files/')


@app.route('/files/', methods=['GET'])
def get_files():
    result = filesManager.src.conectors.files.get_files()
    result = {'files': result}
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=len(result['files']), search=False)

    return render_template('table.html', items=result, navBar=True, pagination=pagination)


@app.route('/files/<_id>/', methods=['DELETE'])
@auth.check_permissions(['delete data'])
def delete_file(_id):
    try:
        filesManager.src.conectors.files.delete_file(_id)
    except FileNotFoundError:
        error = {'error': 'File not found', 'code': 404}
        return render_template('error.html', error=error, navBar=True)
    return redirect('/files/', code=200)


@app.route('/files/<_id>/', methods=['GET'])
def download_file(_id):
    try:
        file = files.get_by_id(_id)
    except FileNotFoundError:
        redirect('/files/')
    return send_file(file.path, as_attachment=True)


@app.before_request
def before_request():
    if request.path in ['/login/', "/"]:
        pass
    else:
        user_token = session.get('token')
        if not user_token:
            return render_template('error.html', error={'error': 'No Token', 'code': 401}, navBar=True)
        else:
            user = u.decode_token(user_token)
            g.role = user['profile']
            g.token = user_token
            g.permissions = user['permissions']


if __name__ == '__main__':
    app.run()
