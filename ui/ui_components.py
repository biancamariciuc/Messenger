import tkinter as tk

def create_title_box(window, content, x, y, size):
    label = tk.Label(window, text=content, font=("Courier New", size))
    # label.place(x=x, y=y)
    label.place(x=x, y=y, anchor="center")



def create_input_box(window, placeholder, x, y, width, height, size):
    entry = tk.Entry(window, font=("Courier New", size), fg="grey")
    entry.insert(0, placeholder)

    def on_focus_in(event):
        current_text = entry.get()
        if current_text == placeholder:
            entry.delete(0, "end")
            entry.config(fg="black")

    # def on_focus_out(event):
    #     current_text = entry.get()
    #     if current_text == "":
    #         entry.insert(0, placeholder)
    #         entry.config(fg="grey")

    entry.bind("<FocusIn>", on_focus_in)
    # entry.bind("<FocusOut>", on_focus_out)

    entry.place(x=x, y=y, width=width, height=height, anchor="center")

    return entry

def create_submit_button(window, text, command, x, y, width, height):
    button = tk.Button(window, text=text, command=command, font=("Courier New", 12, "bold"), bg="#e1e1e1",  cursor="hand2")
    button.place(x=x, y=y, width=width, height=height, anchor="center")
    return button