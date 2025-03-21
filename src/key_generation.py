from Crypto.PublicKey import RSA
import json
import os
from datetime import datetime, timedelta
from dotenv import dotenv_values, set_key

def save_keys_to_env(email, public_key, private_key, zip_name, password_hash, iv_hash_order):
    """
    Guarda las llaves y metadatos en el archivo .env en el formato correcto.
    """
    # Crear la nueva entrada
    expiration_keys = (datetime.now() + timedelta(days=1)).isoformat()
    expiration_file = (datetime.now() + timedelta(days=7)).isoformat()

    new_entry = {
        "public_key": public_key,
        "private_key": private_key,
        "file_encript": {
            "zip_name": zip_name,  # Usamos zip_name en lugar de zip
            "hash_password_zip": password_hash,
            "iv_hash_order": iv_hash_order,
            "expiration_file": expiration_file
        },
        "expiration_keys": expiration_keys
    }

    # Leer el archivo .env
    env_path = ".env"
    try:
        with open(env_path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        # Si el archivo .env no existe, crearlo
        lines = []

    # Buscar la línea que contiene TEMPORARY_KEYS
    temporary_keys_line = None
    for i, line in enumerate(lines):
        if line.startswith("TEMPORARY_KEYS="):
            temporary_keys_line = i
            break

    # Actualizar TEMPORARY_KEYS
    if temporary_keys_line is not None:
        # Cargar los datos existentes
        try:
            existing_data = json.loads(lines[temporary_keys_line].split("=", 1)[1].strip().strip("'"))
        except json.JSONDecodeError:
            # Si hay un error al decodificar, inicializar con una lista vacía
            existing_data = []

        # Buscar si ya existe una entrada para el correo
        email_entry = None
        for entry in existing_data:
            if entry["email"] == email:
                email_entry = entry
                break

        if email_entry:
            # Si ya existe una entrada para el correo, agregar la nueva clave
            email_entry["keys"].append(new_entry)
        else:
            # Si no existe una entrada para el correo, crear una nueva
            email_entry = {
                "email": email,
                "keys": [new_entry]
            }
            existing_data.append(email_entry)

        # Actualizar la línea TEMPORARY_KEYS
        lines[temporary_keys_line] = f"TEMPORARY_KEYS='{json.dumps(existing_data)}'\n"
    else:
        # Si no existe TEMPORARY_KEYS, crear una nueva línea
        email_entry = {
            "email": email,
            "keys": [new_entry]
        }
        lines.append(f"TEMPORARY_KEYS='{json.dumps([email_entry])}'\n")

    # Escribir los cambios en el archivo .env
    with open(env_path, "w") as file:
        file.writelines(lines)

    print("Datos actualizados en el archivo .env.")

def generate_keys(email):
    # Generar par de claves RSA
    key = RSA.generate(2048)
    public_key = key.publickey().export_key().decode()
    private_key = key.export_key().decode()
    return public_key, private_key
