import json
import os

"""Module that takes care of the users"""


def get_clients_history_path():
    """
    Retrun the path if the directory.
    Create the directory if it doesn't exist.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_dir = os.path.dirname(current_dir)
    folder_path = os.path.join(server_dir, "clients_history")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path

def get_users():
    """
    Retrieves the list of registered users from the JSON storage.

    Returns:
        list: A list of dictionaries representing the registered users.
    """
    folder_path = get_clients_history_path()
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
    """Returns true if the user exists in the users list, false otherwise."""
    user_exists = False
    for user in users_list:
        if user["username"] == username:
            user_exists = True
            break
    return user_exists

def search_socket_user(username, dic):
    """Finds the active socket connection for a specific user.."""
    for sock, name in dic.items():
        if name == username:
            return sock
    return None

def handle_login(username):
    """
    Handles the login or registration process for a user.

    Checks if the user is already registered. If not, it adds the username
    to the global users list and creates an empty JSON file for their chat history.
    """

    folder_path = get_clients_history_path()

    users_path = os.path.join(folder_path, "users.json")
    user_history_path = os.path.join(folder_path, f"{username}.json")

    users_list = get_users()

    user_exists = exists_user(username, users_list)

    if user_exists:
        return "Welcome back!"

    else:
        users_list.append({"username": username})
        with open(users_path, "w") as f:
            json.dump(users_list, f, indent=4)

        with open(user_history_path, "w") as f:
            json.dump([], f)

        print(f"Server: Registered new user '{username}'")
        return "Account created!"