import tkinter as tk

"""Module that takes care ot he user list from the left of the window"""

def refresh_user_list(ui_listbox, all_users_data, current_username, search_query=""):
    """
    Updates the listbox with the all users.

    Clears the existing list and repopulates it based on the server data.
    Filters out the current user's name and applies the search query if present.

    Args:
        ui_listbox (tkinter.Listbox): Listbox widget that holds the users
        all_users_data (list): a list of dictionary of all users data
        current_username (str): Current username
        search_query (str, optional): Search query to filter users
    """
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
    """
    Add a user to the listbox

    Args:
        listbox (tkinter.Listbox): Listbox widget that holds the users
        username (str): Username of the clients that has to be added to the listbox
    """
    display_text = f"  {username}"
    listbox.insert(tk.END, display_text)
    last_index = listbox.size() - 1
    listbox.itemconfig(last_index, {'bg': '#f0f0f0', 'fg': 'black'})

def handle_server_user_list(window, user_data_from_server):
    """
    Callback function to update the UI when user data is received from server.

    Args:
        window (tkinter.Toplevel): Toplevel widget that holds the users
        user_data_from_server (list): List of dictionaries of user data
    """
    current_search = window.search_bar.get()
    refresh_user_list(window.user_list, user_data_from_server, window.client.username, current_search)