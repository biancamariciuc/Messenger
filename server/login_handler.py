
from helper_functions.users import *

def handle_login(username):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, "clients_history")
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

