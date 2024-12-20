# services.py
from sqlalchemy import Table, Column, Integer, String, select
from tables import User, Chanel
from database import Base, engine, metadata, init_db, get_db

last_chanel = 0

def register_user(hash_value):
    db = next(get_db())
    user = db.query(User).filter(User.hashing == hash_value).first()
    if user:
        print("Ya fue creado")
    else:
        new_user = User(hashing=hash_value)
        db.add(new_user)
        print("Hash created")
        db.commit()

def get_table_chanel(number):
    name = f'chanel_{number}'
    
    if not engine.dialect.has_table(engine.connect(), name):
        new_table = Table(
            name,
            metadata,
            Column('id', Integer, primary_key=True),
            Column('hashing', String(100))
        )
        global last_chanel
        last_chanel = max(last_chanel, number + 1)
        metadata.create_all(engine)
    return name

def get_last_chanel():
    print(f"Las chanel { last_chanel}")
    return last_chanel

def exist_chanel(number):
    name = f'chanel_{number}'
    return engine.dialect.has_table(engine.connect(), name)

def add_hashing_chanel(num, hashing):
         
    tabla_nombre = get_table_chanel(num)
    tabla = Table(tabla_nombre, metadata, autoload_with=engine)
    
    with engine.begin() as connection:

        query = select(tabla.c.hashing).where(tabla.c.hashing == hashing)
        result = connection.execute(query).fetchone()

        if result is None:  # Si no existe, insertar el valor
            connection.execute(tabla.insert().values(hashing=hashing))
            print(f"Hashing '{hashing}' insertado en la tabla '{tabla_nombre}'.")


