import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import InternalServerError

PWD = os.path.abspath(os.curdir)


if os.name == 'nt' or os.environ.get('OS') == 'Windows_NT':
    UPLOAD_FOLDER = 'C:\SGDF'
else:
    UPLOAD_FOLDER = "/opt/SGDF"
app = Flask(__name__)
app.config.update(SECRET_KEY=os.urandom(24))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/dbase.db'.format(PWD)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.static_folder = 'static'
db = SQLAlchemy(app)


@app.errorhandler(InternalServerError)
def handle_exception(e):
    error = {'error': e, 'code': 500}
    return render_template("error.html", error=error)
