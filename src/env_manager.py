import json
import os
from datetime import datetime, timedelta

def get_private_key_from_env(email, zip_name):
    """
    Obtiene la llave privada del archivo .env para un correo y archivo ZIP específicos.
    """
    temporary_keys_str = os.getenv("TEMPORARY_KEYS")
    if not temporary_keys_str:
        print("Error: No se encontró la variable TEMPORARY_KEYS en el archivo .env.")
        return None

    try:
        temporary_keys = json.loads(temporary_keys_str)
    except json.JSONDecodeError as e:
        print(f"Error al decodificar TEMPORARY_KEYS: {e}")
        return None

    # Buscar el correo en TEMPORARY_KEYS
    for entry in temporary_keys:
        if entry["email"] == email:
            # Buscar la entrada correcta en "keys"
            for key_entry in entry["keys"]:
                if "file_encript" in key_entry and "zip_name" in key_entry["file_encript"]:
                    if key_entry["file_encript"]["zip_name"] == zip_name:
                        return key_entry["private_key"]
                else:
                    print("Error: La estructura de file_encript es incorrecta.")
                    return None

    print(f"Error: No se encontró la llave privada para el correo '{email}' y el archivo ZIP '{zip_name}'.")
    return None

def get_zip_password_from_env(email, zip_name):
    """
    Obtiene la contraseña del archivo .env para un correo y archivo ZIP específicos.
    """
    temporary_keys_str = os.getenv("TEMPORARY_KEYS")
    if not temporary_keys_str:
        print("Error: No se encontró la variable TEMPORARY_KEYS en el archivo .env.")
        return None

    try:
        temporary_keys = json.loads(temporary_keys_str)
    except json.JSONDecodeError as e:
        print(f"Error al decodificar TEMPORARY_KEYS: {e}")
        return None

    # Buscar el correo en TEMPORARY_KEYS
    for entry in temporary_keys:
        if entry["email"] == email:
            # Buscar la entrada correcta en "keys"
            for key_entry in entry["keys"]:
                if "file_encript" in key_entry and "zip_name" in key_entry["file_encript"]:
                    if key_entry["file_encript"]["zip_name"] == zip_name:
                        return key_entry["file_encript"]["hash_password_zip"]
                else:
                    print("Error: La estructura de file_encript es incorrecta.")
                    return None

    print(f"Error: No se encontró la contraseña para el correo '{email}' y el archivo ZIP '{zip_name}'.")
    return None