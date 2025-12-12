import tkinter as tk
FONT = "Courier New"

def create_title_box(window, content, x, y, size):
    label = tk.Label(window, text=content, font=(FONT, size))
    label.place(x=x, y=y, anchor="center")



def create_input_box(window, placeholder, x, y, width, height, size):
    entry = tk.Entry(window, font=(FONT, size), fg="grey")
    entry.insert(0, placeholder)

    def on_focus_in(event):
        current_text = entry.get()
        if current_text == placeholder:
            entry.delete(0, "end")
            entry.config(fg="black")


    entry.bind("<FocusIn>", on_focus_in)

    entry.place(x=x, y=y, width=width, height=height, anchor="center")

    return entry

def create_submit_button(window, text, command, x, y, width, height):
    button = tk.Button(window, text=text, command=command, font=(FONT, 12, "bold"), bg="#e1e1e1",  cursor="hand2")
    button.place(x=x, y=y, width=width, height=height, anchor="center")
    return button


def create_sidebar(window, x, y, width, height):
    frame = tk.Frame(window, width=width, height=height, bg="#f0f0f0")
    frame.place(x=x, y=y)

    user_list = tk.Listbox(frame, font=(FONT, 10), bg="white")
    user_list.place(x=10, y=10, width=width - 20, height=height - 20)

    return user_list

def create_chatbox(window, x, y, width, height):
    frame = tk.Frame(window, width=width, height=height, bg="white")
    frame.place(x=x, y=y)

    chat_display = tk.Text(frame, font=(FONT, 10), bg="#fafafa")
    chat_display.place(x=20, y=20, width=width-40, height=height-80)

    msg_input = tk.Entry(frame, font=(FONT, 10), bg="#f0f0f0")
    msg_input.place(x=20, y=height-50, width=width-110, height=35)

    send_btn = tk.Button(frame, text="Send", font=(FONT, 10, "bold"), bg="#e1e1e1")
    send_btn.place(x=width-80, y=height-50, width=60, height=35)

    return chat_display, msg_input, send_btn

def add_user_to_list(listbox, username):
    display_text = f"  {username}"
    listbox.insert(tk.END, display_text)
    last_index = listbox.size() - 1
    listbox.itemconfig(last_index, {'bg': '#f0f0f0', 'fg': 'black'})