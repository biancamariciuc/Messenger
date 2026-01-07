from client.client import Client
from ui.logic.connect_helper import *
from ui.logic.user_list_helper import *
from ui.logic.message_helper import *
from common.config import SERVER_HOST, SERVER_PORT


from ui.logic.window_helpers import center_window, clear_window
from ui.window_params import WIDTH, HEIGHT, TITLE_X, TITLE_Y, GAP
from ui.ui_components import *

"""The main module that starts the main window."""


class Main_window(tk.Tk):
    """
    The central application class.

    It manages the transition between the Login Screen and the Chat Screen.
    It also establishes the correspondence between network events and UI updates.

    """
    def __init__(self, title):
        """
        Initialize the main window and the network client.

        Sets up the window geometry, initialize the Client connection,
        defines the actions that happens when server sends data.

        Args:
            title: The title displayed in the window  title bar

        """
        super().__init__()
        self.title(title)
        center_window(self, WIDTH, HEIGHT)
        self.client = Client(SERVER_HOST, SERVER_PORT)
        self.client.on_receive_user_list = lambda data: handle_server_user_list(self, data)
        self.client.on_receive_message = lambda sender, content: handle_incoming_message(self, sender, content)
        self.client.on_receive_history = lambda data: handle_history_to_ui(self, data)
        self.selected_user = None
        self.show_login_page()

    def show_login_page(self):
        """
        Shows the initial login screen.

        Clears the window, sets up the username input and the submit (connect) button.
        """
        clear_window(self)
        create_title_box(self, "Welcome!", TITLE_X, TITLE_Y, 30)

        submit_action = lambda event=None: on_click_connect(self)

        self.username = create_input_box(self, "Type here your username...", TITLE_X, TITLE_Y + GAP, 400, 30, 12)
        self.username.bind('<Return>', submit_action)
        create_submit_button(self, "Submit", submit_action, TITLE_X, TITLE_Y + 150, 200, 40)

    def show_message_page(self):
        """
        Show the main chat screen.

        Split the area in 2 parts, left side (sidebar) and right side (message area).
        Bind each button  to their specific logic function.
        """
        clear_window(self)

        sidebar_w = int(WIDTH * 0.3)
        chat_w = WIDTH - sidebar_w

        self.user_list, self.search_bar = create_sidebar(self, x=0, y=0, width=sidebar_w, height=HEIGHT)
        self.user_list.bind('<<ListboxSelect>>', lambda event: on_select_user(self, event))

        search_action = lambda event: self.client.request_users()
        self.search_bar.bind('<Return>', search_action)

        self.client.request_users()

        submit_action = lambda event=None: send_message(self)
        self.chat_display, self.msg_input, self.send_btn, self.chat_header, self.emoji_btn, self.upload_btn = create_chatbox(self, x=sidebar_w, y=0, width=chat_w, height=HEIGHT)
        self.msg_input.bind('<Return>', submit_action)
        self.send_btn.config(command=submit_action)

        self.emoji_btn.config(command=lambda: open_emoji_picker(self))
        self.upload_btn.config(command=lambda: send_image_file(self))


if __name__ == '__main__':
    app = Main_window("Messenger")
    app.mainloop()