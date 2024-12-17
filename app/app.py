from flask import Flask
from flask_jwt_extended import JWTManager
from auth import *
from database import *
from user import User

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'tu_secreto'
#app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=40)
jwt = JWTManager(app)



# Definir el user_lookup_loader para que current_user funcione
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]  # 'sub' es el campo identity del token
    db = next(get_db())  # Obtener la sesión de la base de datos
    return db.query(User).filter(User.username == identity).first()

# Registrar el blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')

# Inicializar la base de datos
init_db()

def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]  # "sub" es el identity definido al crear el token
    db = next(get_db())
    return db.query(User).filter(User.username == identity).first()

if __name__ == '__main__':
    #app.run(debug=True, host="0.0.0.0")
    app.run(debug=True, host='0.0.0.0', port=5000)

