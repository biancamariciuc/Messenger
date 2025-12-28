import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def handle_incoming_message(window, sender, content):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    window.chat_display.config(state=tk.NORMAL)
    window.chat_display.insert(tk.END, f"[{current_time}] {sender}: {content}\n")
    window.chat_display.see(tk.END)
    window.chat_display.config(state=tk.DISABLED)

def send_message(window):
    text = window.msg_input.get()

    if not text:
        return
    if not window.selected_user:
        messagebox.showwarning("Warning", "Please select a user.")
        return

    window.client.send_chat_message(window.selected_user, text)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    window.chat_display.config(state=tk.NORMAL)
    window.chat_display.insert(tk.END, f"[{current_time}] Me: {text}\n")
    window.chat_display.config(state=tk.DISABLED)
    window.chat_display.see(tk.END)

    window.msg_input.delete(0, tk.END)


def handle_history_to_ui(window, history_data):
    window.chat_display.config(state=tk.NORMAL)
    window.chat_display.delete(1.0, tk.END)
    window.chat_display.insert(tk.END, f"\n--- Chatting with {window.selected_user} ---\n")
    for msg in history_data:
        sender = msg["sender"]
        content = msg["content"]
        timestamp = msg["timestamp"]

        window.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {content}\n")

    window.chat_display.config(state=tk.DISABLED)
    window.chat_display.see(tk.END)

def on_select_user(window, event):

    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)

        window.selected_user = data.strip()

        window.chat_display.config(state=tk.NORMAL)
        window.chat_display.delete(1.0, tk.END)
        window.chat_display.insert(tk.END, f"History: {window.selected_user}...\n")
        window.chat_display.config(state=tk.DISABLED)
        window.chat_display.see(tk.END)

        window.client.request_chat_history(window.selected_user)