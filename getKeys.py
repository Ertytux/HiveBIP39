from getpass import getpass
import json
from cryptography.fernet import Fernet
import base64
import hashlib

def generar_clave(password: str) -> bytes:
    # Derivar una clave de 32 bytes a partir de la contraseña
    clave = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(clave)

filex=input('Nombre del archivo cifrado de claves: ')
password=getpass("Password de cifrado: ")

with open(filex, 'r') as archivo:
    keystore = json.load(archivo)

clave = generar_clave(password)
fernet = Fernet(clave)

# Descifrar el texto
texto_descifrado = fernet.decrypt( keystore["cipher"].encode()).decode()

print("Claves: \n", texto_descifrado)