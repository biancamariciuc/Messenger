import json
import os

def get_users():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    folder_path = os.path.join(parent_dir, "clients_history")
    users_path = os.path.join(folder_path, "users.json")

    users_list = []
    if os.path.exists(users_path):
        try:
            with open(users_path, "r") as f:
                users_list = json.load(f)
        except json.JSONDecodeError:
            users_list = []
    return users_list

def exists_user(username, users_list):
    user_exists = False
    for user in users_list:
        if user["username"] == username:
            user_exists = True
            break
    return user_exists

def search_socket_user(username, dic):
    for sock, name in dic.items():
        if name == username:
            return sock
    return None