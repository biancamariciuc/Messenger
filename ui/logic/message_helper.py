import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from client.helper_functions.crypto import decrypt_msg

"""
    Module for handling UI updates and event triggers.
"""

def handle_incoming_message(window, sender, content):
    """
    Handle the incoming message from a user.

    Decrypts the message, formate the message in a pretty format and insert it in the chat_display.

    Args:
        window (tk.Toplevel): The main UI window instance
        sender (str): The sender of the incoming message
        content (str): The content to be inserted in the chat_display
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    decrypted_content = decrypt_msg(content, window.client.private_key)
    window.chat_display.config(state=tk.NORMAL)
    window.chat_display.insert(tk.END, f"{sender}: {decrypted_content}\n", "other_msg")
    window.chat_display.insert(tk.END, f"{current_time}\n\n", "other_time")
    window.chat_display.see(tk.END)
    window.chat_display.config(state=tk.DISABLED)

def send_message(window):
    """
    Handles the logic for sending a message from the UI input.

    Validates that a user is selected, to actually send to someone.
    Trigger the send message logic from client side. And update the UI.

    Args:
        window (tk.Toplevel): The main UI window instance
    """
    text = window.msg_input.get()

    if not text:
        return
    if not window.selected_user:
        messagebox.showwarning("Warning", "Please select a user.")
        return

    window.client.send_chat_message(window.selected_user, text)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    window.chat_display.config(state=tk.NORMAL)
    window.chat_display.insert(tk.END, f"me: {text}\n", "self_msg")
    window.chat_display.insert(tk.END, f"{current_time}\n\n", "self_time")
    window.chat_display.config(state=tk.DISABLED)
    window.chat_display.see(tk.END)

    window.msg_input.delete(0, tk.END)


def handle_history_to_ui(window, history_data):
    """
    Populates the chat window with the conversation history.

    Clears the current display and iterates through the history list.
    Display the messages in a pretty message.

    Args:
        window (tk.Toplevel): The main UI window instance
        history_data (list): A list of history data (messages)
    """
    window.chat_header.config(text=f"Chatting with {window.selected_user}")
    window.chat_display.config(state=tk.NORMAL)
    window.chat_display.delete(1.0, tk.END)
    my_username = window.client.username
    for msg in history_data:
        sender = msg["sender"]
        content = msg["content"]
        timestamp = msg["timestamp"]
        decypted_content = decrypt_msg(content, window.client.private_key)

        if sender == my_username:
            window.chat_display.insert(tk.END, f"me: {decypted_content}\n", "self_msg")
            window.chat_display.insert(tk.END, f"{timestamp}\n\n", "self_time")
        else:
            window.chat_display.insert(tk.END, f"{sender}: {decypted_content}\n", "other_msg")
            window.chat_display.insert(tk.END, f"{timestamp}\n\n", "other_time")

    window.chat_display.config(state=tk.DISABLED)
    window.chat_display.see(tk.END)

def on_select_user(window, event):
    """
    Handles the event when a user is selected from the list.

    Updates the selected user variable, clears the chat window, and
    triggers requests to the server for chat history and the public key.
    Args:
        window (tk.Toplevel): The main UI window instance
        event (tk.Event): The event to be handled
    """
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)

        window.selected_user = data.strip()
        window.chat_header.config(text=f"Chatting with {window.selected_user}")

        window.chat_display.config(state=tk.NORMAL)
        window.chat_display.delete(1.0, tk.END)
        window.chat_display.config(state=tk.DISABLED)
        window.chat_display.see(tk.END)

        window.client.request_chat_history(window.selected_user)
        if window.selected_user not in window.client.users_keys:
            window.client.request_public_key(window.selected_user)