import zipfile
import hashlib
import os

def compress_to_zip(file_path, password):
    zip_name = file_path + '.zip'
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        zipf.write(file_path, os.path.basename(file_path), compress_type=zipfile.ZIP_DEFLATED)
        zipf.setpassword(password.encode())
    return zip_name

def generate_password_hash(email, file_name):
    hash_object = hashlib.sha256((email + file_name).encode())
    return hash_object.hexdigest()