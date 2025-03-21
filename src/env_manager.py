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

def remove_expired_keys():
    """
    Elimina las claves expiradas de la variable TEMPORARY_KEYS en el archivo .env.
    """
    # Leer el archivo .env
    env_path = ".env"
    try:
        with open(env_path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: No se encontró el archivo .env.")
        return

    # Buscar la línea que contiene TEMPORARY_KEYS
    temporary_keys_line = None
    for i, line in enumerate(lines):
        if line.startswith("TEMPORARY_KEYS="):
            temporary_keys_line = i
            break

    if temporary_keys_line is None:
        print("Error: No se encontró la variable TEMPORARY_KEYS en el archivo .env.")
        return

    # Cargar los datos existentes
    try:
        temporary_keys = json.loads(lines[temporary_keys_line].split("=", 1)[1].strip().strip("'"))
    except json.JSONDecodeError as e:
        print(f"Error al decodificar TEMPORARY_KEYS: {e}")
        return

    # Filtrar las claves expiradas
    updated_temporary_keys = []
    for entry in temporary_keys:
        updated_keys = []
        for key_entry in entry["keys"]:
            expiration_keys = datetime.fromisoformat(key_entry["expiration_keys"])
            if expiration_keys > datetime.now():  # Si no ha expirado
                updated_keys.append(key_entry)
        if updated_keys:  # Si aún hay claves no expiradas para este correo
            entry["keys"] = updated_keys
            updated_temporary_keys.append(entry)

    # Actualizar la línea TEMPORARY_KEYS
    lines[temporary_keys_line] = f"TEMPORARY_KEYS='{json.dumps(updated_temporary_keys)}'\n"

    # Escribir los cambios en el archivo .env
    with open(env_path, "w") as file:
        file.writelines(lines)

    print("Claves expiradas eliminadas del archivo .env.")