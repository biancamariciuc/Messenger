import tkinter as tk


def refresh_user_list(ui_listbox, all_users_data, current_username, search_query=""):
    ui_listbox.delete(0, tk.END)

    query = search_query.lower().strip()
    if query == "search...":
        query = ""

    for user_dict in all_users_data:
        name = user_dict.get("username", "Unknown")

        if name == current_username:
            continue

        if query == "" or query in name.lower():
            add_user_to_list(ui_listbox, name)


def add_user_to_list(listbox, username):
    display_text = f"  {username}"
    listbox.insert(tk.END, display_text)
    last_index = listbox.size() - 1
    listbox.itemconfig(last_index, {'bg': '#f0f0f0', 'fg': 'black'})