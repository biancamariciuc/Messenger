import socket
import threading
from common.config import FORMAT, print_log
import json


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.username = None
        self.on_receive_user_list = None
        self.on_receive_message = None
        self.on_receive_history = None

    def connect(self, username):
        try:
            # IPv4, tcp connection
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))

            self.username = username
            self.client_socket.send(username.encode(FORMAT))

            threading.Thread(target=self.listen_for_messages, daemon=True).start()
            return True

        except ConnectionRefusedError:
            print_log("Client error", "server is running?")
        except Exception as e:
            print_log("Client error", str(e))

    def request_users(self):
        if self.client_socket:
            self.client_socket.send("GET_USERS".encode(FORMAT))

    def request_chat_history(self, target_username):
        if self.client_socket:
            format = {"target": target_username}
            msg = f"GET_HISTORY:{json.dumps(format)}"
            self.client_socket.send(msg.encode(FORMAT))

    def send_chat_message(self, receiver_username, message):
        if self.client_socket:
            format = {
                "receiver": receiver_username,
                "content": message
            }
            msg = f"SEND_MSG:{json.dumps(format)}"
            self.client_socket.send(msg.encode(FORMAT))

    def listen_for_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode(FORMAT)

                if message.startswith("LIST_USERS:"):
                    json_str = message.replace("LIST_USERS:", "")
                    data = json.loads(json_str)
                    if self.on_receive_user_list:
                        self.on_receive_user_list(data)
                elif message.startswith("RECEIVE_MSG:"):
                    json_str = message.replace("RECEIVE_MSG:", "")
                    data = json.loads(json_str)

                    sender = data["sender"]
                    content = data["content"]

                    if self.on_receive_message:
                        self.on_receive_message(sender, content)

                elif message.startswith("HISTORY:"):
                    json_str = message.replace("HISTORY:", "")
                    data = json.loads(json_str)

                    if self.on_receive_history:
                        self.on_receive_history(data)

            except Exception as e:
                print_log("Error", "Connection lost")
                break

# if __name__ == "__main__":
#     client = Client(SERVER_HOST, SERVER_PORT)
#     client.connect()