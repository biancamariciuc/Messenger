import rsa
import os
from common.config import *

def generate_keys():
    public_key, private_key = rsa.newkeys(2048)
    return public_key, private_key


def save_keys(username, public_key, private_key):
    if not os.path.exists("keys"):
        os.makedirs("keys")

    with open(f"keys/{username}_public.pem", "wb") as f:
        f.write(public_key.save_pkcs1())

    with open(f"keys/{username}_private.pem", "wb") as f:
        f.write(private_key.save_pkcs1())

def load_keys(username):
    try:
        with open(f"keys/{username}_public.pem", "rb") as f:
            pub = rsa.PublicKey.load_pkcs1(f.read())
        with open(f"keys/{username}_private.pem", "rb") as f:
            priv = rsa.PrivateKey.load_pkcs1(f.read())
        return pub, priv
    except:
        return None, None

def encrypt_msg(message, target_public_key):
    crypto = rsa.encrypt(message.encode(FORMAT), target_public_key)
    return crypto.hex()

def decrypt_msg(hex_message, my_private_key):
    crypto = bytes.fromhex(hex_message)
    return rsa.decrypt(crypto, my_private_key).decode(FORMAT)