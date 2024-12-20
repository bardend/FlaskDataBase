# test_simple.py
import requests

# URL del endpoint
url = 'http://localhost:5000/inviteUser'

# Caso 1: Prueba básica
print("\n=== Prueba invitación de usuario ===")
data = {
    "hash_admi": "admin3",
    "hash_guest": "gues6",
    "name_chanel": "family_chanel"
}

response = requests.post(url, json=data)
print("Respuesta:", response.json())

# Caso 2: Prueba usuario duplicado
print("\n=== Prueba usuario duplicado ===")
data = {
    "hash_admi": "admin3",
    "hash_guest": "gues6",
    "name_chanel": "family_chanel"
}

response = requests.post(url, json=data)
print("Respuesta:", response.json())

# Case 3: Prueba usuario anade a mismo canal
print("\n=== Prueba usuario duplicado ===")
data = {
    "hash_admi": "gues6",
    "hash_guest": "Meeee",
    "name_chanel": "family_chanel"
}

response = requests.post(url, json=data)
print("Respuesta:", response.json())


# Case 4: Prueba usuario anade a otro caanl
print("\n=== Prueba usuario duplicado ===")
data = {
    "hash_admi": "guest456",
    "hash_guest": "Pablooooooo",
    "name_chanel": "home_chanel"
}

response = requests.post(url, json=data)
print("Respuesta:", response.json())

