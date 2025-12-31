import json
import os
from datetime import datetime

"""Module for different actions to the messages."""

def append_to_file(username, msg_format):
    """
    Append messages to a file.

    Search the file by username, append the format of the message

    Args:
        msg_format (str): The format of the message.
        username (str) : The username (unique) for saving the message history.
    """
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

def log_message(sender, receiver, content, is_sender):
    """
        Prepare the message for saving it to the file.

        Creates a format containing the timestamp, sender,
        receiver, and content, then appends it to the user's history log.
    Args:
        sender (str): The username of the client logging the message
        receiver (str): The username of the chat partner.
        content (str): The content of the message
        is_sender (bool): Whether the message is sender or receiver
        """
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    msg_format = {
        "sender": sender if is_sender else receiver,
        "receiver": receiver if is_sender else sender,
        "timestamp": time,
        "content": content
    }

    append_to_file(sender, msg_format)

def get_chat_history(sender, receiver):
    """
    Retrieve the chat history between sender and receiver.

    Args:
        sender (str): The username of the client logging the message
        receiver (str): The username of the chat partner.
    Returns:
        conversation (list): The conversation of the message
    """
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