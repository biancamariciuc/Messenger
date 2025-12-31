import rsa
import os
import json
from common.config import FORMAT
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

"""
Module for handling message encryption and decryption.

Implements a mechanism to encrypt and decrypt messages using a hybrid AES + RSA approach.
A random, one-time AES key is generated to encrypt the message content (CBC mode).
The AES key is then encrypted using the RSA public key, allowing
the client to decrypt it using their private key to access the message.

"""


def generate_keys():
    """Generate keys ( public key and private key )."""
    public_key, private_key = rsa.newkeys(1024)
    return public_key, private_key


def save_keys(username, public_key, private_key):
    """
    Save keys in pem files

    Create (if it does not exist) a directory where we can save keys
    """
    if not os.path.exists("keys"):
        os.makedirs("keys")

    with open(f"keys/{username}_public.pem", "wb") as f:
        f.write(public_key.save_pkcs1())

    with open(f"keys/{username}_private.pem", "wb") as f:
        f.write(private_key.save_pkcs1())

def load_keys(username):
    """Load keys from pem files"""
    try:
        with open(f"keys/{username}_public.pem", "rb") as f:
            pub = rsa.PublicKey.load_pkcs1(f.read())
        with open(f"keys/{username}_private.pem", "rb") as f:
            priv = rsa.PrivateKey.load_pkcs1(f.read())
        return pub, priv
    except:
        return None, None

# !!!! cod generat cu AI !!!!!

def encrypt_msg(message, target_public_key):
    """
    Encrypt message using hybrid AES + RSA approach

    Generate the one-time AES key and encrypt the message content (CBC mode).
    Then, encrypts the AES key itself using the RSA public key.

    Args:
        message : text to be encrypted
        target_public_key : recipient public key to encrypt
    Return:
        a package that contains the encrypted the unique vector, encrypted message and the encrypted AES key.
        all data converted to hex for json.
    """
    try:
        aes_key = get_random_bytes(32)

        cipher_aes = AES.new(aes_key, AES.MODE_CBC)
        iv = cipher_aes.iv

        encrypted_bytes = cipher_aes.encrypt(pad(message.encode(FORMAT), AES.block_size))

        encrypted_aes_key = rsa.encrypt(aes_key, target_public_key)

        package = {
            "iv": iv.hex(),
            "ciphertext": encrypted_bytes.hex(),
            "key": encrypted_aes_key.hex()
        }

        return json.dumps(package)

    except Exception as e:
        print(f"Encryption Error: {e}")
        return ""


def decrypt_msg(package_str, my_private_key):
    """
    Decrypt message using hybrid AES + RSA approach

    Parses the JSON package to extract the unique vector iv,  encrypted AES key and ciphertext.
    Uses the RSA private key to recover the AES session key, which is then
    used to decrypt the actual message content.

    Args:
        package_str: package string that contains the essentials for the decryption
        my_private_key: private key to decrypt the ciphertext
    Return:
        a package that contains the decrypted the unique vector, decrypted message and the AES key.
    """
    try:
        package = json.loads(package_str)

        iv = bytes.fromhex(package["iv"])
        ciphertext = bytes.fromhex(package["ciphertext"])
        encrypted_aes_key = bytes.fromhex(package["key"])

        aes_key = rsa.decrypt(encrypted_aes_key, my_private_key)

        cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)

        decrypted_text = unpad(cipher_aes.decrypt(ciphertext), AES.block_size).decode(FORMAT)

        return decrypted_text

    except Exception as e:
        print(f"Decryption Error: {e}")
        return "[Error: Message corrupted or wrong key]"