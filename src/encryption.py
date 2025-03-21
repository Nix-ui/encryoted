from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from env_manager import remove_expired_keys
import os

def encrypt_file(file_path, public_key,outputh_name =None):
    # Generar una clave simétrica aleatoria
    remove_expired_keys()
    session_key = get_random_bytes(16)

    # Cifrar la clave simétrica con la clave pública
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Cifrar los datos con AES
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    with open(file_path, 'rb') as f:
        data = f.read()
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    # Guardar el archivo cifrado
    if outputh_name is None:
        encrypted_file = file_path + '.enc'
    else:
        encrypted_file = outputh_name
    with open(encrypted_file, 'wb') as f:
        [f.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]

    return encrypted_file, cipher_aes.nonce.hex()