import os
from common.config import print_log

"""Module for saving and retrieving user public keys."""

def save_user_pub_key(username, key_data):
    """Saves the public key of a user to the disk."""
    try:
        with open(f"server_keys/{username}.pem", "w") as f:
            f.write(key_data)
    except Exception as e:
        print_log("Error", f"Could not save key for")


def get_user_pub_key_from_disk(username):
    """Retrieves the public key of a user from the disk."""
    try:
        if os.path.exists(f"server_keys/{username}.pem"):
            with open(f"server_keys/{username}.pem", "r") as f:
                return f.read()
    except Exception as e:
        return e
    return None