import json
import os
from datetime import datetime


def append_to_file(username, msg_format):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    folder_path = os.path.join(parent_dir, "clients_history")
    file_path = os.path.join(folder_path, f"{username}.json")

    history = []
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                history = json.load(f)
        except:
            history = []

    history.append(msg_format)
    try:
        with open(file_path, "w") as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        print(e)

def log_message(sender, receiver, content):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    msg_format = {
        "sender": sender,
        "receiver": receiver,
        "timestamp": time,
        "content": content
    }

    append_to_file(sender, msg_format)
    append_to_file(receiver, msg_format)


def get_chat_history(sender, receiver):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    folder_path = os.path.join(parent_dir, "clients_history")
    file_path = os.path.join(folder_path, f"{sender}.json")

    conversation = []

    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                all_messages = json.load(f)

            for msg in all_messages:
                if (msg["sender"] == receiver) or (msg["receiver"] == receiver):
                    conversation.append(msg)
        except Exception as e:
            print(e)

    return conversation