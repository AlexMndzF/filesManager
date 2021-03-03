from sqlalchemy import Column, Integer, String, DateTime,  Float

from filesManager.settings import db


class User(db.Model):
    """User on app"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    profile = Column(String(100), nullable=False)
    permissions = Column(String(100), nullable=False)


class File(db.Model):
    """Files table"""
    __tablename__ = 'pdfs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    weigth = Column(Float, nullable=False)
    hash = Column(String, nullable=False)
    upload_date = Column(DateTime, nullable=False)
    path = Column(String(100), nullable=False)
