from beem import Hive
from beem.account import Account
from beemgraphenebase.account import PasswordKey

from hdwallet import HDWallet
from hdwallet.entropies import BIP39Entropy


from hdwallet.cryptocurrencies import Bitcoin as Cryptocurrency
from hdwallet.hds import BIP44HD

from getpass import getpass
import json
from cryptography.fernet import Fernet
import base64
import hashlib

nodes = [
    "https://api.deathwing.me",
    "https://api.openhive.network",
    "https://hive-api.arcange.eu",
    "https://techcoderx.com",
    "https://api.hive.blog"
]

user = input("Introduzca su nombre de usuario: ")
opasswd = getpass('Introduzca su clave privada Owner: ')

hdwallet = HDWallet(cryptocurrency=Cryptocurrency,
                    hd=BIP44HD,).from_entropy(
    entropy=BIP39Entropy(entropy=BIP39Entropy.generate(
        strength=256
    )))

mnemonic = hdwallet.mnemonic()
print("\n\n")
print(
    f"Guarde con seguridad las siguientes {len(mnemonic.split())} palabras:\n")
print(f"Úselas para importar su cuenta en Hive-KeyChain, KeyStore de Inleo y otras billeteras \n")
print(mnemonic)
print("\n\n")
# New Keys
owner_key = PasswordKey(user, mnemonic, role='owner').get_private_key()
active_key = PasswordKey(user, mnemonic, role='active').get_private_key()
posting_key = PasswordKey(user, mnemonic, role='posting').get_private_key()
memo_key = PasswordKey(user, mnemonic, role='memo').get_private_key()


data = {'username': f"{user}",
        'owner': f"{owner_key._wif}",
        'active': f"{active_key._wif}",
        'posting': f"{posting_key._wif}",
        'memo': f"{memo_key._wif}",
        'password': f"{mnemonic}"}

pspass = getpass("Password de cifrado de su archivo keystore: ")


def generar_clave(password: str) -> bytes:
    # Derivar una clave de 32 bytes a partir de la contraseña
    clave = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(clave)


clave = generar_clave(pspass)

fernet = Fernet(clave)

texto_cifrado = fernet.encrypt(str(data).encode())

keystore = {
    "cipher": texto_cifrado.decode()
}

userfile = f"{user}_HIVE_cf.json"
with open(userfile, 'w') as archivo:
    json.dump(keystore, archivo, indent=4)


print(
    f'\n\n PD: Guarde con seguridad el archivo {userfile} y recuerde la contraseña utilizada\n')

hive = Hive(node=nodes,keys=[opasswd])

account = Account(user, blockchain_instance=hive)

account.update_account_keys(new_password=mnemonic)

print("Done.")
