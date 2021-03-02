import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

ALLOWED_EXTENSIONS = {'pdf'}
PWD = os.path.abspath(os.curdir)


if os.name == 'nt' or os.environ.get('OS') == 'Windows_NT':
    UPLOAD_FOLDER = 'C:\SGDF'
else:
    UPLOAD_FOLDER = "/opt/SGDF"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/dbase.db'.format(PWD)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER