from flask import Flask
from flask_jwt_extended import JWTManager
from auth import *
from database import *

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'tu_secreto'
jwt = JWTManager(app)

# Registrar el blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')

# Inicializar la base de datos
init_db()

if __name__ == '__main__':
    app.run(debug=True)

