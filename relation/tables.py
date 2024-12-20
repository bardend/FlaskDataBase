# tables.py
from database import Base, engine, metadata
from sqlalchemy import Column, Integer, String, Table, Boolean

class User(Base):
    __tablename__ = 'users3'
    id = Column(Integer, primary_key=True)
    hashing = Column(String(100), nullable=True)
    family_chanel = Column(Integer, default=0)
    home_chanel = Column(Integer, default=0)
    extra_chanel = Column(Integer, default=0)

class Chanel(Base):
    __tablename__ = 'list_chanels'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)

