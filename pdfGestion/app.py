from flask import Flask, request, Response, g
from flask_sqlalchemy import SQLAlchemy
from pdfGestion import config
from pdfGestion.src import sql

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


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
def create_pdf():
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
