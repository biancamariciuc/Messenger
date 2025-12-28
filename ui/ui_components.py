import tkinter as tk
FONT = "Courier New"

def create_title_box(window, content, x, y, size):
    label = tk.Label(window, text=content, font=(FONT, size))
    label.place(x=x, y=y, anchor="center")



def create_input_box(window, placeholder, x, y, width, height, size, anch="center"):
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
    button = tk.Button(window, text=text, command=command, font=(FONT, 12, "bold"), bg="#e1e1e1",  cursor="hand2")
    button.place(x=x, y=y, width=width, height=height, anchor="center")
    return button


def create_sidebar(window, x, y, width, height):
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

    emoji_btn = tk.Button(frame, text="😊", font=(FONT, 12), bg="#e1e1e1", cursor="hand2")
    emoji_btn.place(x=20, y=height - 50, width=35, height=35)

    image_btn = tk.Button(frame, text="📷", font=(FONT, 12), bg="#e1e1e1", cursor="hand2")
    image_btn.place(x=60, y=height - 50, width=35, height=35)

    send_btn = tk.Button(frame, text="Send", font=(FONT, 10, "bold"), bg="#e1e1e1", cursor="hand2")
    send_btn.place(x=width - 80, y=height - 50, width=60, height=35)

    return chat_display, msg_input, send_btn, header_label, emoji_btn, image_btn
