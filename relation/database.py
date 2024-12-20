# database.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database():
    # Conexión al servidor PostgreSQL por defecto
    conn = psycopg2.connect(
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    cursor = conn.cursor()
    
    try:
        # Intentar crear la base de datos
        cursor.execute("CREATE DATABASE relation")
        print("Base de datos 'relation' creada exitosamente")
    except psycopg2.errors.DuplicateDatabase:
        print("La base de datos 'relation' ya existe")
    finally:
        cursor.close()
        conn.close()

Base = declarative_base()
metadata = MetaData()

# URL de conexión
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:123@localhost:5432/relation')

# Crear la base de datos si no existe
create_database()

# Crear el engine después de asegurarnos que la base de datos existe
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
