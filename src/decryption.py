from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import zipfile
import pathlib
from env_manager import get_private_key_from_env,get_zip_password_from_env,remove_expired_keys

def decrypt_file(encrypted_file, private_key,output_file):
    remove_expired_keys()
    with open(encrypted_file, 'rb') as f:
        enc_session_key = f.read(256)  # Tamaño de la clave RSA
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    # Descifrar la clave simétrica con la clave privada
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Descifrar los datos con AES
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)

    # Guardar el archivo descifrado
    file_extension = pathlib.Path(encrypted_file).suffix
    decrypted_file = encrypted_file.replace(file_extension, output_file)
    with open(decrypted_file, 'wb') as f:
        f.write(data)
    return decrypted_file

def unzip_and_decrypt(email, zip_name, output_file):
    """
    Descomprime el archivo ZIP y descifra el archivo usando la llave privada.
    """
    # Obtener la llave privada del archivo .env
    zip_password = get_zip_password_from_env(email, zip_name)
    private_key = get_private_key_from_env(email, zip_name)
    if not private_key:
        print("Error: No se encontró la llave privada para el correo y archivo ZIP especificados.")
        return

    # Descomprimir el archivo ZIP
    try:
        with zipfile.ZipFile(zip_name, 'r') as zipf:
            zipf.extractall(pwd=zip_password.encode())
            encrypted_file = zipf.namelist()[0]  # Obtener el nombre del primer archivo en el ZIP
    except Exception as e:
        print(f"Error al descomprimir el archivo ZIP: {e}")
        return

    # Descifrar el archivo
    decrypted_file = decrypt_file(encrypted_file, private_key, output_file)
    if decrypted_file:
        print(f"Archivo descifrado guardado como: {decrypted_file}")