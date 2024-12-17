# client.py
import requests
import json
import hashlib

class AuthClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None

    def create_account(self, username: str, password: str) -> dict:
        """Crear una nueva cuenta de usuario."""
        url = f"{self.base_url}/auth/createAccount"
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        payload = {
            "username": username,
            "passwordHash": password_hash
        }
        
        response = requests.post(url, json=payload)
        return {
            "status_code": response.status_code,
            "response": response.json()
        }

    def login(self, username: str, password: str) -> dict:
        """Iniciar sesión y obtener tokens."""
        url = f"{self.base_url}/auth/login"
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        payload = {
            "username": username,
            "passwordHash": password_hash
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get('accessToken')
            self.refresh_token = data.get('refreshToken')
        
        return {
            "status_code": response.status_code,
            "response": response.json()
        }

    def refresh_access_token(self) -> dict:  # Cambiamos el nombre del método
        """Refrescar el token de acceso."""
        if not self.refresh_token:
            return {"error": "No refresh token available. Please login first."}
        
        url = f"{self.base_url}/auth/refresh-token"
        headers = {
            "Authorization": f"Bearer {self.refresh_token}"
        }
        
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get('accessToken')
        
        return {
            "status_code": response.status_code,
            "response": response.json()
        }

    def get_headers(self):
        """Obtener headers con el token de acceso."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def my_info(self):
        
        url = f"{self.base_url}/auth/who_am_i"

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        response = requests.get(url, headers=headers)

        return {
            "status_code": response.status_code,
            "response": response.json()
        }

    def prube(self):
        url = f"{self.base_url}/auth/who_am_i2"

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
       
        response = requests.get(url, headers=headers)

        return {
            "status_code": response.status_code,
            "response": response.json()
        }


if __name__ == "__main__":
    # Crear instancia del cliente
    client = AuthClient()
    
    # Definir datos de prueba
    test_username = "u112::"
    test_password = "1421"
    
    # 1. Crear cuenta
    print("\n1. Creando cuenta...")
    create_result = client.create_account(test_username, test_password)
    print(json.dumps(create_result, indent=2))
    
    # 2. Iniciar sesión
    print("\n2. Iniciando sesión...")
    login_result = client.login(test_username, test_password)
    print(json.dumps(login_result, indent=2))
    
    # 3. Refrescar token
    print("\n3. Refrescando token...")
    refresh_result = client.refresh_access_token()  # Usamos el nuevo nombre del método
    print(json.dumps(refresh_result, indent=2))

    print("Vamos a ver mi info")
    inf = client.my_info()
    print(json.dumps(inf, indent=2))

    xd = client.prube()
    print(json.dumps(xd, indent=2))
