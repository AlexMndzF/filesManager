from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy import DateTime,  Text, Float
from sqlalchemy.orm import relationship

from pdfGestion.app import db


class User(db.Model):
    """User od app"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    profile = Column(String(100), nullable=False)
    permissions = Column(String(100), nullable=False)


class Pdf(db.Model):
    """pdfs"""
    __tablename__ = 'pdfs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    weigth = Column(Float, nullable=False)
    has = Column(String, nullable=False)
    upload_date = Column(DateTime, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
