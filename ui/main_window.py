from client.client import Client
from ui.logic.connect_helper import *
from common.config import SERVER_HOST, SERVER_PORT
from server.helper_functions.users import get_users


from ui.window_helpers import center_window, clear_window
from ui.window_params import WIDTH, HEIGHT, TITLE_X, TITLE_Y, GAP
from ui.ui_components import *


class Main_window(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        center_window(self, WIDTH, HEIGHT)
        self.client = Client(SERVER_HOST, SERVER_PORT)
        self.show_login_page()

    def show_login_page(self):
        clear_window(self)
        create_title_box(self, "Welcome!", TITLE_X, TITLE_Y, 30)

        self.username = create_input_box(self, "Type here your username...", TITLE_X, TITLE_Y + GAP, 400, 30, 12)
        create_submit_button(self, "Login", lambda: on_click_connect(self), TITLE_X, TITLE_Y + 150, 200, 40)

    def show_message_page(self):
        clear_window(self)

        sidebar_w = int(WIDTH * 0.3)
        chat_w = WIDTH - sidebar_w

        self.user_list = create_sidebar(self, x=0, y=0, width=sidebar_w, height=HEIGHT)
        users_list = get_users()
        current_user = self.client.username

        for user_dict in users_list:
            username = user_dict.get("username", "Unknown")
            if username == current_user:
                continue
            add_user_to_list(self.user_list, username)

        self.chat_display, self.msg_input, self.send_btn = create_chatbox(self, x=sidebar_w, y=0, width=chat_w, height=HEIGHT)

        self.send_btn.config(command=self.send_message)

    def send_message(self):
        print("Message sent!")

if __name__ == '__main__':
    app = Main_window("Messenger")
    app.mainloop()