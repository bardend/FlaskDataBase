import jwt
from sqlalchemy.orm import Session
from user import *
from security import *
from database import *

def register_user(data):
    username = data.get('username')
    password_hash = data.get('passwordHash')
    
    db = next(get_db())
    
    if not username or not password_hash:
        return {'message': 'Invalid data', 'status': 400}

    if db.query(User).filter(User.username == username).first() :
        return {'message': 'User already exists', 'status': 400}
    
    new_user = User(username=username, password_hash=password_hash, rol = 'guest')
    db.add(new_user)
    db.commit()

    return {'message': 'User registered successfully', 'status': 201}


def login_user(data):
    username = data.get('username')
    password_hash = data.get('passwordHash')
    
    db = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password_hash != password_hash:
        return {'message': 'Invalid login', 'status':400}

    return {'username': username, 'status': 200}


