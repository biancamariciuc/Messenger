from tkinter import messagebox

def on_click_connect(window):
    """
    Handles the logic when the login button is clicked.

    Retrieves the username entered by the user and calls the connection function
    to establish a session with the server.
    """
    username = window.username.get()

    if not username:
        messagebox.showwarning("Warning", "Please enter a username.")
        return

    success = window.client.connect(username)

    if success:
        messagebox.showinfo("Success", f"Connected as {username}!")
        window.show_message_page()
    else:
        messagebox.showerror("Error", "Could not connect to server.\nIs it running?")