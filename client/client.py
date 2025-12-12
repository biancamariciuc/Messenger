import socket
import threading
from common.config import FORMAT, print_log


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.username = None

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

    def listen_for_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode(FORMAT)
                print(message)
            except Exception as e:
                print_log("Error", "Connection lost")
                break

# if __name__ == "__main__":
#     client = Client(SERVER_HOST, SERVER_PORT)
#     client.connect()