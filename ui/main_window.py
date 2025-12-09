import tkinter as tk
from tkinter import messagebox

from ui.window_helpers import center_window, clear_window
from ui.window_params import WIDTH, HEIGHT, TITLE_X, TITLE_Y, GAP
from ui.ui_components import create_title_box, create_input_box, create_submit_button


class Main_window(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        center_window(self, WIDTH, HEIGHT)
        self.show_login_page()

    def show_login_page(self):
        clear_window(self)
        create_title_box(self, "Welcome!", TITLE_X, TITLE_Y, 30)

        self.username = create_input_box(self, "Type here your username...", TITLE_X, TITLE_Y + GAP, 400, 30, 15)
        create_submit_button(self, "Login", self.login_page, TITLE_X, TITLE_Y + 150, 200, 40)

    def login_page(self):
        user = self.username.get()
        if user == "":
            messagebox.showerror("Error", "Please enter a valid username.")
        else:
            print(f"{user} logged in")

if __name__ == '__main__':
    app = Main_window("Messenger")
    app.mainloop()