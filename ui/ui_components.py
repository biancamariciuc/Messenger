import tkinter as tk
from ui.logic.window_helpers import center_emoji_window
FONT = "Courier New"
FONT_EMOJI = "Segoe UI Emoji"

"""Module that defines and handles all visual components used in the application."""

def create_title_box(window, content, x, y, size):
    """
    Creates a title for the first window shown to the user

    Args:
        window: the window to show
        content: the actual title
        x: the x position of the window
        y: the y position of the window
        size: the size of the window
    """
    label = tk.Label(window, text=content, font=(FONT, size))
    label.place(x=x, y=y, anchor="center")



def create_input_box(window, placeholder, x, y, width, height, size, anch="center"):
    """
    Creates the input box where the user can write either the message either the ID.

    Args:
        window: the window to show
        placeholder: the placeholder text
        x: the x position of the window
        y: the y position of the window
        width: the width of the window
        height: the height of the window
        size: the size of the window
        anch: the anchor to use, by default it is set to "center"
    """
    entry = tk.Entry(window, font=(FONT, size), fg="grey")
    entry.insert(0, placeholder)

    def on_focus_in(event):
        current_text = entry.get()
        if current_text == placeholder:
            entry.delete(0, "end")
            entry.config(fg="black")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")


    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    entry.place(x=x, y=y, width=width, height=height, anchor=anch)

    return entry

def create_submit_button(window, text, command, x, y, width, height):
    """
    Created a submit button.
    Args:
        window: the window to show
        text: the text to show
        command: the command to run, the actual action
        x: the x position of the button
        y: the y position of the button
        width: the width of the button
        height: the height of the button
    Returns:
        button: the component button to be used
    """
    button = tk.Button(window, text=text, command=command, font=(FONT, 12, "bold"), bg="#e1e1e1",  cursor="hand2")
    button.place(x=x, y=y, width=width, height=height, anchor="center")
    return button


def create_sidebar(window, x, y, width, height):
    """
    Creates the sidebar, the component that displays the list of connected users.

    Args:
        window: the window that is used
        x:  the position x
        y: the position y
        width: the width of the sidebar
        height: the height of the sidebar

    Returns:
        user_list: the Listbox component that is used for showing the users
        search_entry: the Entry where a user can search for a specific user
    """
    frame = tk.Frame(window, width=width, height=height, bg="#f0f0f0")
    frame.place(x=x, y=y)

    search_entry = tk.Entry(frame, font=(FONT, 10), bg="#f0f0f0", fg="black", relief="flat")
    search_entry.place(x=10, y=15, width=width - 20, height=30)
    placeholder = "Search..."
    search_entry.insert(0, placeholder)

    def on_focus_in(event):
        if search_entry.get() == placeholder:
            search_entry.delete(0, "end")
            search_entry.config(fg="black")

    def on_focus_out(event):
        if search_entry.get() == "":
            search_entry.insert(0, placeholder)
            search_entry.config(fg="grey")

    search_entry.bind("<FocusIn>", on_focus_in)
    search_entry.bind("<FocusOut>", on_focus_out)

    user_list = tk.Listbox(frame, font=(FONT, 10), bg="#f0f0f0")
    user_list.place(x=10, y=60, width=width - 20, height=height - 70)

    return user_list, search_entry

def create_chatbox(window, x, y, width, height):
    """
    Creates the main visual part of the chat interface.

    This function assembles the message display area, the input field,
    and the action buttons (Send, Emoji, Image).

    Args:
        window: The parent window
        x: the x position
        y: the y position
        width: the width of the chatbox area
        height: the height of the chatbox area

    Returns:
        chat_display: the Text widget where messages appear
        msg_input: the Entry widget for typing messages
        send_btn: the Send Button widget
        header_label: the Label showing the current chat partner
        emoji_btn: the Button for opening emojis
        image_btn: the Button for sending images

    """
    frame = tk.Frame(window, width=width, height=height, bg="#f0f0f0")
    frame.place(x=x, y=y)

    header_label = tk.Label(frame, text="Select a user", font=(FONT, 12, "bold"), bg="#e1e1e1", anchor="center")
    header_label.place(x=0, y=0, width=width, height=40)

    chat_display = tk.Text(frame, font=(FONT, 10), bg="#fafafa")
    chat_display.place(x=20, y=45, width=width-40, height=height-100)

    chat_display.tag_configure("self_msg", justify='right', foreground="blue", lmargin1=50)
    chat_display.tag_configure("self_time", justify='right', foreground="grey", font=(FONT, 8))

    chat_display.tag_configure("other_msg", justify='left', foreground="black", rmargin=50)
    chat_display.tag_configure("other_time", justify='left', foreground="grey", font=(FONT, 8))

    input_x = 105
    send_btn_width = 60
    input_width = width - input_x - send_btn_width - 30
    msg_input = create_input_box(frame, "Type a message...", input_x, height-50, input_width, 35, 10, anch="nw")

    emoji_btn = tk.Button(frame, text="😊", font=(FONT_EMOJI, 12), bg="#e1e1e1", cursor="hand2")
    emoji_btn.place(x=20, y=height - 50, width=35, height=35)

    image_btn = tk.Button(frame, text="📷", font=(FONT_EMOJI, 12), bg="#e1e1e1", cursor="hand2")
    image_btn.place(x=60, y=height - 50, width=35, height=35)

    send_btn = tk.Button(frame, text="Send", font=(FONT, 10, "bold"), bg="#e1e1e1", cursor="hand2")
    send_btn.place(x=width - 80, y=height - 50, width=60, height=35)

    return chat_display, msg_input, send_btn, header_label, emoji_btn, image_btn


def create_picker_window(parent):
    """
    Creates the window structure for the Emoji Picker.
    It includes a Canvas and Scrollbar to allow scrolling through many emojis.

    Args:
        parent: The main window

    Returns:
        pop: The Toplevel window instance
        container: The internal Frame where buttons should be placed
    """
    title = "Emoji Picker"
    pop = tk.Toplevel(parent)
    pop.title(title)
    center_emoji_window(pop, parent, 460, 350)

    cvs = tk.Canvas(pop)
    bar = tk.Scrollbar(pop, orient="vertical", command=cvs.yview)
    container = tk.Frame(cvs)

    container.bind("<Configure>", lambda e: cvs.configure(scrollregion=cvs.bbox("all")))
    cvs.create_window((0, 0), window=container, anchor="nw")
    cvs.configure(yscrollcommand=bar.set)

    cvs.pack(side="left", fill="both", expand=True)
    bar.pack(side="right", fill="y")

    return pop, container