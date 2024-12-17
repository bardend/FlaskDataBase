from functools import wraps
from user import User
from database import *
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from audit_logging import  log_event, setup_log


setup_log()

# Decorador para verificar el rol
def role_required(required_role):
    def decorator(func):
        @wraps(func)  # Mantiene el nombre y las propiedades de la función decorada
        def wrapper(*args, **kwargs):

            auth_header = request.headers.get('Authorization')

            if not auth_header:
                return jsonify({"error": "Missing token in headers."}), 400

            try:
                token = auth_header.split(" ")[1]
                # Decodificar el token y extraer la identidad del usuario
                identity = get_jwt_identity()  # Este es el valor que has puesto en el 'identity' al crear el token
                db = next(get_db())
                persona = db.query(User).filter(User.username==identity).first()

                if not persona: 
                    return jsonify({"error": "User not found."}), 404
                if persona.rol != required_role:
                    return jsonify({"error": "Access denied. Insufficient permissions."}), 403

                return func(*args, **kwargs)
            
            except Exception as e:
                return jsonify({"error": "Invalid or expired token."}), 401

        return wrapper
    return decorator

def audit_log(action) :
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # En este caso el header puede ser de 2 tipos:
            # 1. Authorization que envia un token el cual saco el usuario como rol required
            # 2. username que me da un string 
            # En este caso yo quiero imprimir el nombre del usuario

            token = request.headers.get('Authorization')
            user_name = request.json.get('username', None)

            if token:
                token = auth_header.split(" ")[1]
                identity = get_jwt_identity()  # Decodifica el token para obtener el usuario
                user = identity
            elif user_name:
                user = user_name
            else :
                return jsonify({"error": "Missing user information."}), 400

            retval =  func(*args, **kwargs)


            if retval:

                if retval[1] == 200 or retval[1] == 201:
                    log_event(
                        level="info",
                        message=f"OK - Action: {action}, User: {user}, Endpoint: {request.path}"
                    )
                else:
                    log_event(
                        level="error",
                        message=f"ERROR - Status: {retval[1]}, Action: {action}, User: {user}, Endpoint: {request.path}\n {json.loads(retval[0].get_data().decode('utf-8'))}"
                    )
            return retval
        return wrapper
    return decorator
