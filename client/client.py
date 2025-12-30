import socket
import threading
from common.config import FORMAT, print_log
from client.helper_functions.crypto import *
import json
import time


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.username = None
        self.on_receive_user_list = None
        self.on_receive_message = None
        self.on_receive_history = None
        self.public_key = None
        self.private_key = None
        self.users_keys = {}

    def connect(self, username):
        try:
            pub, priv = load_keys(username)
            if not pub:
                pub, priv = generate_keys()
                save_keys(username, pub, priv)

            self.public_key = pub
            self.private_key = priv

            # IPv4, tcp connection
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))

            self.username = username
            self.client_socket.send(username.encode(FORMAT))

            time.sleep(0.1)

            pem_key = self.public_key.save_pkcs1().decode(FORMAT)
            msg = f"PUB_KEY:{pem_key}"
            self.client_socket.send(msg.encode(FORMAT))

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

    def request_public_key(self, target_user):
        msg = f"GET_KEY:{target_user}"
        self.client_socket.send(msg.encode(FORMAT))

    def send_chat_message(self, receiver_username, message):
        if self.client_socket:
            if receiver_username not in self.users_keys:
                self.request_public_key(receiver_username)
                return
            receiver_pub_key = self.users_keys[receiver_username]
            encrypted_for_them = encrypt_msg(message, receiver_pub_key)
            encrypted_for_me = encrypt_msg(message, self.public_key)
            format = {
                "receiver": receiver_username,
                "msg_for_receiver": encrypted_for_them,
                "msg_for_sender": encrypted_for_me
            }
            msg = f"SEND_MSG:{json.dumps(format)}"
            self.client_socket.send(msg.encode(FORMAT))

    def listen_for_messages(self):
        while True:
            try:
                message = self.client_socket.recv(16384).decode(FORMAT)

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
                elif message.startswith("KEY_RESPONSE:"):
                    json_str = message.replace("KEY_RESPONSE:", "")
                    data = json.loads(json_str)
                    target = data["user"]
                    pk = data["key"]
                    self.users_keys[target] = rsa.PublicKey.load_pkcs1(pk.encode(FORMAT))

            except Exception as e:
                print_log("Error", "Connection lost")
                break

# if __name__ == "__main__":
#     client = Client(SERVER_HOST, SERVER_PORT)
#     client.connect()