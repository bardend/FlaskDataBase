# client.py
import requests
import json

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

    def refresh_token(self) -> dict:
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


# Ejemplo de uso
if __name__ == "__main__":
    import hashlib
    
    # Crear instancia del cliente
    client = AuthClient()
    
    # Definir datos de prueba
    test_username = "usuario_prueba"
    test_password = "contraseña123"
    
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
    refresh_result = client.refresh_token()
    print(json.dumps(refresh_result, indent=2))
    
    # Ejemplo de manejo de errores
    print("\n4. Probando crear cuenta duplicada...")
    duplicate_result = client.create_account(test_username, test_password)
    print(json.dumps(duplicate_result, indent=2))
