from Crypto.PublicKey import RSA
import json
import os
from datetime import datetime, timedelta
from dotenv import dotenv_values, set_key

def save_keys_to_env(email, public_key, private_key, zip_name, password_hash, iv_hash_order):
    # Crear la estructura de datos
    new_entry = {
        "email": email,
        "keys": [{
            "public_key": public_key,
            "private_key": private_key,
            "file_encript": {
                "hash_password_zip": password_hash,
                "zip_name": zip_name,
                "iv_hash_order": iv_hash_order,
                "expiration_file": (datetime.now() + timedelta(days=1)).isoformat()
            },
            "expiration_keys": (datetime.now() + timedelta(days=1)).isoformat()
        }]
    }

    # Leer el archivo .env
    env_vars = dotenv_values(".env")
    temporary_keys_str = env_vars.get("TEMPORARY_KEYS", "[]")

    # Convertir TEMPORARY_KEYS a una lista de Python
    try:
        temporary_keys = json.loads(temporary_keys_str)
    except json.JSONDecodeError:
        temporary_keys = []

    # Agregar la nueva entrada
    temporary_keys.append(new_entry)

    # Convertir la lista actualizada a una cadena JSON
    updated_temporary_keys_str = json.dumps(temporary_keys)

    # Actualizar la variable TEMPORARY_KEYS en el archivo .env
    set_key(".env", "TEMPORARY_KEYS", updated_temporary_keys_str)

def generate_keys(email):
    # Generar par de claves RSA
    key = RSA.generate(2048)
    public_key = key.publickey().export_key().decode()
    private_key = key.export_key().decode()
    return public_key, private_key
