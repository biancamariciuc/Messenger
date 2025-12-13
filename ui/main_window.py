from client.client import Client
from ui.logic.connect_helper import *
from ui.logic.update_user_list import *
from common.config import SERVER_HOST, SERVER_PORT


from ui.window_helpers import center_window, clear_window
from ui.window_params import WIDTH, HEIGHT, TITLE_X, TITLE_Y, GAP
from ui.ui_components import *


class Main_window(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        center_window(self, WIDTH, HEIGHT)
        self.client = Client(SERVER_HOST, SERVER_PORT)
        self.client.on_receive_user_list = self.handle_server_user_list
        self.show_login_page()

    def show_login_page(self):
        clear_window(self)
        create_title_box(self, "Welcome!", TITLE_X, TITLE_Y, 30)

        self.username = create_input_box(self, "Type here your username...", TITLE_X, TITLE_Y + GAP, 400, 30, 12)
        create_submit_button(self, "Login", lambda: on_click_connect(self), TITLE_X, TITLE_Y + 150, 200, 40)

    def handle_server_user_list(self, user_data_from_server):
        current_search = self.search_bar.get()
        refresh_user_list(self.user_list, user_data_from_server, self.client.username, current_search)

    def show_message_page(self):
        clear_window(self)

        sidebar_w = int(WIDTH * 0.3)
        chat_w = WIDTH - sidebar_w

        self.user_list, self.search_bar = create_sidebar(self, x=0, y=0, width=sidebar_w, height=HEIGHT)

        search_action = lambda event: self.client.request_users()
        self.search_bar.bind('<Return>', search_action)

        self.client.request_users()

        self.chat_display, self.msg_input, self.send_btn = create_chatbox(self, x=sidebar_w, y=0, width=chat_w, height=HEIGHT)
        self.send_btn.config(command=self.send_message)
    def send_message(self):
        print("Message sent!")

if __name__ == '__main__':
    app = Main_window("Messenger")
    app.mainloop()