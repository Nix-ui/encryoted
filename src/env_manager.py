import json
import os
from datetime import datetime, timedelta

def get_private_key_from_env(email, zip_name):
    """
    Obtiene la llave privada del archivo .env para un correo y archivo ZIP específicos.
    """
    temporary_keys_str = os.getenv("TEMPORARY_KEYS")
    if not temporary_keys_str:
        return None

    temporary_keys = json.loads(temporary_keys_str)
    for entry in temporary_keys:
        if entry["email"] == email:
            for key_entry in entry["keys"]:
                if key_entry["file_encript"]["zip_name"] == zip_name:
                    return key_entry["private_key"]
    return None

def get_zip_password_from_env(email, zip_name):
    """
    Obtiene la contraseña del archivo .env para un correo y archivo ZIP específicos.
    """
    temporary_keys_str = os.getenv("TEMPORARY_KEYS")
    if not temporary_keys_str:
        return None
    temporary_keys = json.loads(temporary_keys_str)
    for entry in temporary_keys:
        if entry["email"] == email:
            for key_entry in entry["keys"]:
                if key_entry["file_encript"]["zip_name"] == zip_name:
                    return key_entry["file_encript"]["hash_password_zip"]
    return None