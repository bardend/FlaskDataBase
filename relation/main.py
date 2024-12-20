from flask import Flask
from endpoints import configure_routes
from database import init_db

app = Flask(__name__)

# Configurar los endpoints
configure_routes(app)
# Inicializar la base de datos
init_db()


if __name__ == '__main__':
    app.run(debug=True)

