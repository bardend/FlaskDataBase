# auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity,
    current_user
)
from sqlalchemy.orm import Session
from user import *
from security import *
from database import *

from services import register_user, login_user
from decorators import role_required




auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/createAccount', methods=['POST'])
def create_account():
    data = request.json
    return jsonify(register_user(data))
    

@auth_bp.route('/login', methods=['POST'])
def login():
    res = login_user(request.json)

    if res['status'] == 200 :
        access_token = create_access_token(identity=res['username'])
        refresh_token = create_refresh_token(identity=res['username'])
        return jsonify(accessToken=access_token, refreshToken=refresh_token), 200

    return jsonify({"message": "Usuario o contraseña incorrectos"}), 401

@auth_bp.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
#Rol -- logg
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(accessToken=new_access_token), 200

# Ruta protegida que utiliza current_user
@auth_bp.route("/who_am_i", methods=["GET"])
@jwt_required()
def who_am_i():
    if not current_user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    return jsonify(
        id=current_user.id,
        username=current_user.username,
        password_hash=current_user.password_hash,
        rol=current_user.rol,
    ), 200

# Ruta protegida que utiliza current_user
@auth_bp.route("/get_rol", methods=["GET"])
@jwt_required()
def get_rol():
    if not current_user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    return jsonify(
        rol=current_user.rol,
    ), 200


@auth_bp.route("/who_am_i2", methods=["GET"])
@jwt_required()  # Asegura que el usuario está autenticado con un token JWT válido
@role_required('guest')  # Verifica que el usuario tenga el rol 'guest'
def go():

    return jsonify(
        id=2,
    ), 200
