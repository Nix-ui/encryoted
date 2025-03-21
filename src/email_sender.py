import os
import json
import base64
from sendgrid import SendGridAPIClient
from dotenv import load_dotenv
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

def send_email(to_email, zip_name):
    # Crear el mensaje de correo
    message = Mail(
        from_email=os.getenv("SENDER_EMAIL"),
        to_emails=to_email,
        subject="Archivo cifrado",
        html_content="Adjunto encontrarás el archivo cifrado."
    )

    # Leer y codificar el archivo ZIP en base64
    with open(zip_name, 'rb') as f:
        data = f.read()
    encoded_file = base64.b64encode(data).decode()

    # Adjuntar el archivo ZIP
    attached_file = Attachment(
        FileContent(encoded_file),
        FileName(zip_name),
        FileType('application/zip'),
        Disposition('attachment')
    )
    message.attachment = attached_file

    # Enviar el correo
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"Correo enviado. Código de estado: {response.status_code}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        
        # Cargar variables de entorno
load_dotenv()

def is_email_in_whitelist(email):
    # Obtener la whitelist del archivo .env
    whitelist_str = os.getenv("WHITE_LIST_EMAILS")
    if not whitelist_str:
        return False

    # Convertir la whitelist a una lista de diccionarios
    whitelist = json.loads(whitelist_str)
    
    # Verificar si el correo está en la whitelist
    return any(entry["email"] == email for entry in whitelist)