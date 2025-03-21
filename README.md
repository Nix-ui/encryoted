# Requisitos
* Programa que utilize un cifrado hibrido para encriptar archivos pdf
* Debe generar llaves temporales
* El archivo resultante del cifrado debe tener un tiempo de vida
* El archivo resultante deben comprimirse en un zip y mandarse por correo
    * Se usa SENDGRID como servicio email el email remitentente es una variable de entorno
    * el zip debe cifrarse con una contraseña la cual es el hash del correo electronico y el nombre del archivo original
* El programa guarda las claves y los archivos resultantes en el archivo .env en el siguiente formato:
    * ```JSON
        TEMPORARY_KEYS=[{
        "email":"algo@correo.com",
        "keys":[{
            "public_key": "asdfafas",
            "private_key":"gdgdwerewf",
            "file_encript":{
                "hash_password_zip":"fgdfhqergf",
                "zip_name": "dadasda.algo",
                "iv_hash_order":"adasdasdas",
                "expiration_file":"date",
            },
            "expiration_keys":"date"
            } 
          ]
         }
        ]
* Las llaves privadas deben ser generadas apartir de un email los cuales estan en una white list en el archivo.env
* Los archivos deben dividirse por funcionalidad
* El decifrado debe generar el archivo general con un nombre dado
* Debe crearse una carpeta de logs donde se registraran los logs por fecha y deben incluir el remitente, el nombre del zip mandado , el destinatario, y la fecha