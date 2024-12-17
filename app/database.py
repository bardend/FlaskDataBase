#database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user import Base

from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:123@localhost:5432/watch_man')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
