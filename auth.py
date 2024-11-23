# auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from sqlalchemy.orm import Session
from user import *
from security import *
from database import *

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/createAccount', methods=['POST'])
def create_account():
    data = request.get_json()
    username = data.get('username')
    password_hash = data.get('passwordHash')
    
    db = next(get_db())
    
    if db.query(User).filter(User.username == username).first():
        return jsonify({"message": "Usuario ya existe"}), 400
    
    new_user = User(username=username, password_hash=password_hash)
    db.add(new_user)
    db.commit()
    
    return jsonify({"message": "Cuenta creada con éxito"}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password_hash = data.get('passwordHash')
    
    db = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    
    if not user or user.password_hash != password_hash:
        return jsonify({"message": "Usuario o contraseña incorrectos"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(accessToken=access_token, refreshToken=refresh_token), 200


@auth_bp.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(accessToken=new_access_token), 200
