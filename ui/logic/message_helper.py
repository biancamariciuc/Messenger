import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from client.helper_functions.crypto import decrypt_msg
import base64
import io
from PIL import Image, ImageTk
from ui.window_params import EMOJIS
from ui.ui_components import create_picker_window


"""
    Module for handling UI updates and event triggers and multimedia data.
"""

def compress_image(file_path):
    """
    Reads an image from a file path, compresses it, and encodes it to a string.

    This function opens the image, converts it to RGB format, resizes it,
    and converts the binary data into a Base64 string
    so it can be saved in a JSON object.

    Args:
        file_path: path to the image
    Returns:
        final_string: compressed image encoded as a Base64 string
    """
    if not file_path or isinstance(file_path, tuple):
        return None
    try:
        with open(file_path, "rb") as f:
            original_img = Image.open(f)
            rgb_img = original_img.convert("RGB")
            rgb_img.thumbnail((250, 250))

            buffer = io.BytesIO()
            rgb_img.save(buffer, format="JPEG", quality=70)

            img_bytes = buffer.getvalue()
            encoded_image = base64.b64encode(img_bytes  )
            final_string = encoded_image.decode('utf-8')
            return final_string
    except Exception as e:
        print(f"Error image: {e}")
        return None


def display_content(window, sender, content, tag_msg, tag_time):
    """
    Helper function to display conversation content in a formatted way.

   It checks the content type:
    - If it is an image, it performs the inverse process of the compress function
      (decodes Base64) and displays the photo.
    - If it is normal text, it inserts it directly into the chat.

    Args:
        window: The main UI window instance.
        sender: the username of the image seender
        content: the text message or the Base64 string of an image.
        tag_msg: tag message - 'self_msg' or 'other_msg'
        tag_time: tag time
    """
    if content.startswith("[IMAGE]:"):
        try:
            base64_data = content.replace("[IMAGE]:", "")
            img_bytes = base64.b64decode(base64_data)
            memory_buffer = io.BytesIO(img_bytes)
            pil_image = Image.open(memory_buffer)
            photo = ImageTk.PhotoImage(pil_image)

            if not hasattr(window, "images"):
                window.images = []
            window.images.append(photo)

            window.chat_display.insert(tk.END, f"{sender}:\n", tag_msg)
            window.chat_display.image_create(tk.END, image=photo)
            window.chat_display.insert(tk.END, "\n")
        except Exception as e:
            window.chat_display.insert(tk.END, f"{sender}: [Image Error]\n", tag_msg)
    else:
        window.chat_display.insert(tk.END, f"{sender}: {content}\n", tag_msg)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    window.chat_display.insert(tk.END, f"{current_time}\n\n", tag_time)

def handle_incoming_message(window, sender, content):
    """
    Handle the incoming message from a user.

    Decrypts the message, formate the message in a pretty format and insert it in the chat_display.

    Args:
        window (tk.Toplevel): The main UI window instance
        sender (str): The sender of the incoming message
        content (str): The content to be inserted in the chat_display
    """
    decrypted_content = decrypt_msg(content, window.client.private_key)
    window.chat_display.config(state=tk.NORMAL)
    display_content(window, sender, decrypted_content, "other_msg", "other_time")
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


    window.chat_display.config(state=tk.NORMAL)
    display_content(window, "me", text, "self_msg", "self_time")
    window.chat_display.config(state=tk.DISABLED)
    window.chat_display.see(tk.END)

    window.msg_input.delete(0, tk.END)

def send_image_file(window):
    """
    Logic for selecting, processing, and sending an image.

    This function opens a file dialog for the user to select an image,
    calls the compress_image function, sends it to the selected user
    via the client socket, and updates  display.
    """

    file_path = filedialog.askopenfilename(
        title="Select image",
        filetypes=[("Images", "*.jpg *.jpeg *.png")]
    )

    base64_str = compress_image(file_path)

    if base64_str:
        msg_content = f"[IMAGE]:{base64_str}"
        window.client.send_chat_message(window.selected_user, msg_content)
        window.chat_display.config(state=tk.NORMAL)
        display_content(window, "me", msg_content, "self_msg", "self_time")
        window.chat_display.see(tk.END)
        window.chat_display.config(state=tk.DISABLED)



def populate_emojis(target_frame, input_field):
    """
    Helper function that populates the picker window with emojis.

    This function iterates through the global EMOJIS list and creates a button
    for each one. It uses a grid system to arrange them (6 items per row)
    """
    r = 0
    c = 0
    for em in EMOJIS:
        btn = tk.Button(
            target_frame,
            text=em,
            font=("Segoe UI Emoji", 12),
            width=4,
            command=lambda x=em: input_field.insert(tk.END, x)
        )
        btn.grid(row=r, column=c, padx=2, pady=2)

        c += 1
        if c > 5:
            c = 0
            r += 1

def open_emoji_picker(window):
    """
    Open the picker window and populate it.
    """
    picker, emoji = create_picker_window(window)
    populate_emojis(emoji, window.msg_input)


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
    window.images = []
    for msg in history_data:
        sender = msg["sender"]
        content = msg["content"]
        decrypted_content = decrypt_msg(content, window.client.private_key)

        if sender == my_username:
            display_content(window, "me", decrypted_content, "self_msg", "self_time")
        else:
            display_content(window, sender, decrypted_content, "other_msg", "other_time")

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