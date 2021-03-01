from flask import Flask, request, Response, g
from flask_sqlalchemy import SQLAlchemy
from pdfGestion import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


from pdfGestion.src import sql
from pdfGestion.src import authorization as auth

@app.route('/login/', methods=['POST'])
def check_user():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        token = sql.check_loging(username=username, password=password)
    except TypeError as e:
        return Response(response="User not exist", status=400)
    return Response(response=token, status=200)


@app.route('/pdf/', methods=['POST'])
def upload_pdf():
    pass

@app.route('/pdf/', methods=['GET'])
def get_pdfs():
    pass

@app.route('/pdf/<id>/', methods=['DELETE'])
@auth.check_permissions(['delete data'])
def delete_pdfs(id):
    pass


@app.before_request
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


if __name__ == '__main__':
    app.run()
