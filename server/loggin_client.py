import json
import os

def handle_login(username):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, "clients_history")
    full_path = os.path.join(folder_path, f"{username}.json")

    if not os.path.exists(full_path):
        with open(full_path, "w") as f:
            json.dump([], f)
        return "Account created!"
    else:
        return "Welcome back!"