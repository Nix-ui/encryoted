import os
import json
import zipfile
from dotenv import load_dotenv, set_key, dotenv_values
from encryption import encrypt_file
from key_generation import generate_keys, save_keys_to_env
from file_handler import compress_to_zip, generate_password_hash
from email_sender import send_email, is_email_in_whitelist
from logging_handler import log_action
from decryption import unzip_and_decrypt
from env_manager import get_private_key_from_env




def main():
    # Datos de entrada
    email = input("Ingrese el correo del destinatario: ")
    file_path = input("Ingrese la ruta del archivo PDF a cifrar: ")

    # Verificar si el correo está en la whitelist
    if not is_email_in_whitelist(email):
        print("Error: El correo no está en la whitelist.")
        return

    # Generar llaves temporales
    public_key, private_key = generate_keys(email)

    # Cifrar el archivo
    encrypted_file, iv_hash_order = encrypt_file(file_path, public_key)

    # Generar contraseña para el ZIP
    password_hash = generate_password_hash(email, os.path.basename(file_path))

    # Comprimir el archivo cifrado en un ZIP
    zip_name = compress_to_zip(encrypted_file, password_hash)

    # Enviar el ZIP por correo
    send_email(email, zip_name)

    # Guardar las claves y metadatos en el archivo .env
    save_keys_to_env(email, public_key, private_key, zip_name, password_hash, iv_hash_order)

    # Registrar la acción en los logs
    log_action(email, zip_name, os.getenv("SENDER_EMAIL"))

    print("Proceso completado. Archivo cifrado y enviado por correo.")



if __name__ == "__main__":
    while True:
        print("\n=== Menú Principal ===")
        print("1. Cifrar y enviar archivo")
        print("2. Descifrar archivo recibido")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opción (1-3): ")
        
        if opcion == "1":
            main()
        elif opcion == "2":
            email = input("Ingrese su correo electrónico: ")
            zip_path = input("Ingrese la ruta del archivo ZIP: ")
            outputh_file = input("Ingrese la salida del archivo: ")
            unzip_and_decrypt(email, zip_path, outputh_file)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intente nuevamente.")    