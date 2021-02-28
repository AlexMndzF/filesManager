from flask import Flask, request, Response
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
    except Exception as e:
        print(e)
        e
    return Response(response=token, status=200)


if __name__ == '__main__':
    app.run()
