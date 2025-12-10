from tkinter import messagebox

def on_click_connect(window):

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