import unittest
from unittest.mock import Mock
from ..models import User
from ..src.conectors.users import check_login
from ..settings import db
from ..src.exceptions import InvalidPasswordException, UserNotExistException


def add_data_tables_test():
    db.create_all()
    user_admin = User(name='test', password='test', profile='admin', permissions='delete data')

    db.session.add(user_admin)
    db.session.commit()


db.drop_all()
db.create_all()
add_data_tables_test()


class TestUser(unittest.TestCase):

    def test_check_login_ok(self):
        token_test = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEsIm5hbWUiOiJ0ZXN0IiwicHJvZmlsZSI6ImFkbWluIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlIGRhdGEiXX0.S_XSXspfraWna8UrMx9ApsJo5b1XM-a4TL0ObF0wFIw'
        token = check_login('test', 'test')
        assert(token, token_test)

    def test_check_login_invalid_user(self):
        with self.assertRaises(UserNotExistException):
            check_login('test_fail', 'test')

    def test_check_login_invalid_password(self):
        with self.assertRaises(InvalidPasswordException):
            check_login('test', 'test_fail')
