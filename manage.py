from flask_script import Manager
from pdfGestion.app import app
from pdfGestion.models import *

manager = Manager(app)
app.config['DEBUG'] = True  # Ensure debugger will load.


@manager.command
def create_tables():
    "Create relational database tables."
    db.create_all()


@manager.command
def drop_tables():
    "Drop all project relational database tables. THIS DELETES DATA."
    db.drop_all()


@manager.command
def add_data_tables():
    db.create_all()
    user_admin = User(name='admin', password='admin', profile='admin', permissions='delete data')
    user_user = User(name='user', password='user', profile='user', permissions='view data')

    db.session.add(user_admin)
    db.session.commit()
    db.session.add(user_user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()